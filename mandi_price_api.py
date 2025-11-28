"""
Mandi Price API Integration
Fetches real-time commodity prices from data.gov.in (Government of India Open Data)
Coverage: 2500+ mandis across India with daily price updates
"""

import requests
import sqlite3
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import os
from dotenv import load_dotenv

load_dotenv()

class MandiPriceAPI:
    """
    Integration with data.gov.in API for real-time mandi prices
    """
    
    # API Configuration
    BASE_URL = "https://api.data.gov.in/resource"
    RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"  # Daily commodity prices
    
    # Mapping of our ingredients to commodity names used in mandi data
    INGREDIENT_TO_COMMODITY = {
        # Grains & Cereals
        "Rice": "Rice",
        "Wheat": "Wheat",
        "Jowar": "Jowar(Sorghum)",
        "Bajra": "Bajra(Pearl Millet)",
        "Ragi": "Ragi (Finger Millet)",
        "Maize": "Maize",
        
        # Pulses
        "Moong Dal": "Green Gram Dal (Moong Dal)",
        "Toor Dal": "Arhar (Tur/Red Gram)(Whole)",
        "Chana Dal": "Bengal Gram Dal (Chana Dal)",
        "Urad Dal": "Black Gram Dal (Urad Dal)",
        "Masoor Dal": "Lentil (Masur)(Whole)",
        "Kidney Beans": "Kulthi(Horse Gram)",
        "Chickpeas": "Bengal Gram(Gram)(Whole)",
        "Black Eyed Peas": "Cowpea (Lobia)",
        
        # Vegetables
        "Potato": "Potato",
        "Tomato": "Tomato",
        "Onion": "Onion",
        "Carrot": "Carrot",
        "Spinach": "Spinach",
        "Brinjal": "Brinjal",
        "Cabbage": "Cabbage",
        "Cauliflower": "Cauliflower",
        "Beans": "Beans",
        "Peas": "Peas Wet",
        "Drumstick": "Drumstick",
        "Bitter Gourd": "Bitter gourd",
        "Bottle Gourd": "Bottle gourd",
        "Ladies Finger": "Ladies Finger",
        "Capsicum": "Capsicum",
        "Cucumber": "Cucumber(Kheera)",
        "Pumpkin": "Pumpkin",
        "Radish": "Radish",
        "Beetroot": "Beet Root",
        "Sweet Potato": "Sweet Potato",
        "Green Chilli": "Green Chilli",
        "Ginger": "Ginger(Green)",
        "Garlic": "Garlic",
        "Coriander Leaves": "Coriander(Leaves)",
        "Curry Leaves": "Curry Leaf",
        "Methi Leaves": "Methi(Leaves)",
        
        # Fruits
        "Banana": "Banana",
        "Apple": "Apple",
        "Orange": "Orange",
        "Mango": "Mango",
        "Papaya": "Papaya",
        "Guava": "Guava",
        "Pomegranate": "Pomegranate",
        "Grapes": "Grapes",
        "Watermelon": "Water Melon",
        "Sapota": "Sapota",
        "Lemon": "Lemon",
        "Coconut": "Coconut",
        
        # Dairy (usually not in mandi, but adding for reference)
        "Milk": "Milk",
        "Curd": "Curd/Yoghurt",
        
        # Oils & Others
        "Groundnut": "Groundnut",
        "Coconut Oil": "Coconut Oil",
        "Mustard Oil": "Mustard Oil",
        "Jaggery": "Jaggery",
        "Sugar": "Sugar",
        "Tamarind": "Tamarind Fruit",
        
        # Eggs & Non-Veg (limited availability)
        "Eggs": "Egg Hen(NECC)",
        "Chicken": "Chicken",
        "Fish": "Fish",
        
        # Nuts & Seeds
        "Almonds": "Almond(Badam)",
        "Cashew": "Cashewnuts",
        "Peanuts": "Groundnut",
    }
    
    # Karnataka state mandis for local prices
    KARNATAKA_MANDIS = [
        "Hubli", "Dharwad", "Belgaum", "Mysore", "Bangalore", 
        "Gulbarga", "Davangere", "Shimoga", "Mangalore", "Bellary",
        "Raichur", "Bijapur", "Gadag", "Haveri", "Koppal"
    ]
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with API key"""
        self.api_key = api_key or os.getenv('DATA_GOV_API_KEY')
        self.db_path = os.path.join(os.path.dirname(__file__), 'nutrition_advisor.db')
        self._ensure_price_table()
    
    def _ensure_price_table(self):
        """Create price history table if not exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mandi_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                commodity TEXT NOT NULL,
                state TEXT,
                district TEXT,
                market TEXT,
                variety TEXT,
                min_price REAL,
                max_price REAL,
                modal_price REAL,
                arrival_date TEXT,
                fetched_at TEXT,
                UNIQUE(commodity, market, arrival_date)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingredient_price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ingredient_name TEXT NOT NULL,
                price_per_kg REAL NOT NULL,
                source TEXT DEFAULT 'mandi',
                market TEXT,
                state TEXT,
                recorded_date TEXT,
                fetched_at TEXT,
                UNIQUE(ingredient_name, market, recorded_date)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def fetch_mandi_prices(self, commodity: str = None, state: str = "Karnataka", 
                           limit: int = 100) -> List[Dict]:
        """
        Fetch current mandi prices from data.gov.in API
        
        Args:
            commodity: Specific commodity to search (optional)
            state: State to filter by (default: Karnataka)
            limit: Number of records to fetch
            
        Returns:
            List of price records
        """
        if not self.api_key:
            print("Warning: No API key configured. Using cached/sample data.")
            return self._get_sample_prices()
        
        try:
            params = {
                "api-key": self.api_key,
                "format": "json",
                "limit": limit,
                "offset": 0
            }
            
            # Add filters
            filters = []
            if state:
                filters.append(f"state:{state}")
            if commodity:
                filters.append(f"commodity:{commodity}")
            
            if filters:
                params["filters[state]"] = state
                if commodity:
                    params["filters[commodity]"] = commodity
            
            url = f"{self.BASE_URL}/{self.RESOURCE_ID}"
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                records = data.get("records", [])
                
                # Cache the fetched data
                self._cache_prices(records)
                
                return records
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return self._get_cached_prices(commodity, state)
                
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return self._get_cached_prices(commodity, state)
    
    def _cache_prices(self, records: List[Dict]):
        """Cache fetched prices to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for record in records:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO mandi_prices 
                    (commodity, state, district, market, variety, min_price, max_price, modal_price, arrival_date, fetched_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    record.get('commodity', ''),
                    record.get('state', ''),
                    record.get('district', ''),
                    record.get('market', ''),
                    record.get('variety', ''),
                    float(record.get('min_price', 0) or 0),
                    float(record.get('max_price', 0) or 0),
                    float(record.get('modal_price', 0) or 0),
                    record.get('arrival_date', ''),
                    datetime.now().isoformat()
                ))
            except Exception as e:
                print(f"Cache error for {record.get('commodity')}: {e}")
        
        conn.commit()
        conn.close()
    
    def _get_cached_prices(self, commodity: str = None, state: str = None) -> List[Dict]:
        """Get prices from cache"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM mandi_prices WHERE 1=1"
        params = []
        
        if commodity:
            query += " AND commodity LIKE ?"
            params.append(f"%{commodity}%")
        if state:
            query += " AND state = ?"
            params.append(state)
        
        query += " ORDER BY fetched_at DESC LIMIT 100"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        # Convert to dict format
        columns = ['id', 'commodity', 'state', 'district', 'market', 'variety', 
                   'min_price', 'max_price', 'modal_price', 'arrival_date', 'fetched_at']
        return [dict(zip(columns, row)) for row in rows]
    
    def _get_sample_prices(self) -> List[Dict]:
        """Return sample prices when API is not available"""
        # Sample Karnataka mandi prices (approximate values in Rs/Quintal)
        sample_data = [
            {"commodity": "Rice", "state": "Karnataka", "market": "Hubli", "modal_price": 3500, "min_price": 3200, "max_price": 3800},
            {"commodity": "Wheat", "state": "Karnataka", "market": "Hubli", "modal_price": 2800, "min_price": 2600, "max_price": 3000},
            {"commodity": "Potato", "state": "Karnataka", "market": "Hubli", "modal_price": 2000, "min_price": 1800, "max_price": 2200},
            {"commodity": "Tomato", "state": "Karnataka", "market": "Hubli", "modal_price": 2500, "min_price": 2000, "max_price": 3000},
            {"commodity": "Onion", "state": "Karnataka", "market": "Hubli", "modal_price": 1800, "min_price": 1500, "max_price": 2100},
            {"commodity": "Banana", "state": "Karnataka", "market": "Hubli", "modal_price": 3000, "min_price": 2500, "max_price": 3500},
            {"commodity": "Bengal Gram(Gram)(Whole)", "state": "Karnataka", "market": "Hubli", "modal_price": 6500, "min_price": 6000, "max_price": 7000},
            {"commodity": "Green Gram Dal (Moong Dal)", "state": "Karnataka", "market": "Hubli", "modal_price": 8000, "min_price": 7500, "max_price": 8500},
            {"commodity": "Groundnut", "state": "Karnataka", "market": "Hubli", "modal_price": 5500, "min_price": 5000, "max_price": 6000},
            {"commodity": "Jowar(Sorghum)", "state": "Karnataka", "market": "Hubli", "modal_price": 3200, "min_price": 3000, "max_price": 3500},
            {"commodity": "Ragi (Finger Millet)", "state": "Karnataka", "market": "Hubli", "modal_price": 3800, "min_price": 3500, "max_price": 4200},
            {"commodity": "Spinach", "state": "Karnataka", "market": "Hubli", "modal_price": 2000, "min_price": 1500, "max_price": 2500},
            {"commodity": "Carrot", "state": "Karnataka", "market": "Hubli", "modal_price": 3000, "min_price": 2500, "max_price": 3500},
            {"commodity": "Cabbage", "state": "Karnataka", "market": "Hubli", "modal_price": 1500, "min_price": 1200, "max_price": 1800},
            {"commodity": "Cauliflower", "state": "Karnataka", "market": "Hubli", "modal_price": 2500, "min_price": 2000, "max_price": 3000},
        ]
        return sample_data
    
    def get_ingredient_price(self, ingredient_name: str, market: str = "Hubli") -> Optional[Dict]:
        """
        Get current price for an ingredient
        
        Args:
            ingredient_name: Name of ingredient from our database
            market: Mandi/market name
            
        Returns:
            Price info dict or None
        """
        # Map ingredient to commodity name
        commodity = self.INGREDIENT_TO_COMMODITY.get(ingredient_name)
        
        if not commodity:
            return None
        
        # Fetch prices for this commodity
        prices = self.fetch_mandi_prices(commodity=commodity, state="Karnataka")
        
        # Find price for specified market or nearest available
        for price in prices:
            if market.lower() in price.get('market', '').lower():
                # Convert from Rs/Quintal to Rs/kg
                modal_price_per_kg = float(price.get('modal_price', 0)) / 100
                return {
                    'ingredient': ingredient_name,
                    'commodity': commodity,
                    'market': price.get('market'),
                    'state': price.get('state'),
                    'price_per_kg': modal_price_per_kg,
                    'min_price_per_kg': float(price.get('min_price', 0)) / 100,
                    'max_price_per_kg': float(price.get('max_price', 0)) / 100,
                    'arrival_date': price.get('arrival_date'),
                    'source': 'data.gov.in'
                }
        
        # If no exact match, return first available
        if prices:
            price = prices[0]
            modal_price_per_kg = float(price.get('modal_price', 0)) / 100
            return {
                'ingredient': ingredient_name,
                'commodity': commodity,
                'market': price.get('market'),
                'state': price.get('state'),
                'price_per_kg': modal_price_per_kg,
                'min_price_per_kg': float(price.get('min_price', 0)) / 100,
                'max_price_per_kg': float(price.get('max_price', 0)) / 100,
                'arrival_date': price.get('arrival_date'),
                'source': 'data.gov.in'
            }
        
        return None
    
    def update_all_ingredient_prices(self, market: str = "Hubli") -> Dict:
        """
        Update prices for all mapped ingredients
        
        Returns:
            Summary of updated prices
        """
        updated = []
        failed = []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for ingredient, commodity in self.INGREDIENT_TO_COMMODITY.items():
            try:
                price_info = self.get_ingredient_price(ingredient, market)
                
                if price_info and price_info['price_per_kg'] > 0:
                    # Update ingredient_price_history
                    cursor.execute('''
                        INSERT OR REPLACE INTO ingredient_price_history
                        (ingredient_name, price_per_kg, source, market, state, recorded_date, fetched_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        ingredient,
                        price_info['price_per_kg'],
                        'data.gov.in',
                        price_info['market'],
                        price_info['state'],
                        price_info.get('arrival_date', datetime.now().strftime('%Y-%m-%d')),
                        datetime.now().isoformat()
                    ))
                    
                    # Also update main ingredients table
                    cursor.execute('''
                        UPDATE ingredients SET cost = ? WHERE name = ?
                    ''', (price_info['price_per_kg'], ingredient))
                    
                    updated.append({
                        'ingredient': ingredient,
                        'new_price': price_info['price_per_kg'],
                        'market': price_info['market']
                    })
                else:
                    failed.append(ingredient)
                    
            except Exception as e:
                print(f"Error updating {ingredient}: {e}")
                failed.append(ingredient)
        
        conn.commit()
        conn.close()
        
        return {
            'updated_count': len(updated),
            'failed_count': len(failed),
            'updated_ingredients': updated,
            'failed_ingredients': failed
        }
    
    def get_price_trends(self, ingredient_name: str, days: int = 30) -> List[Dict]:
        """
        Get historical price trends for an ingredient
        
        Args:
            ingredient_name: Name of ingredient
            days: Number of days of history
            
        Returns:
            List of price records
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        cursor.execute('''
            SELECT ingredient_name, price_per_kg, market, state, recorded_date
            FROM ingredient_price_history
            WHERE ingredient_name = ? AND fetched_at >= ?
            ORDER BY recorded_date DESC
        ''', (ingredient_name, cutoff_date))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'ingredient': row[0],
                'price_per_kg': row[1],
                'market': row[2],
                'state': row[3],
                'date': row[4]
            }
            for row in rows
        ]
    
    def get_cheapest_markets(self, ingredient_name: str) -> List[Dict]:
        """
        Find cheapest markets for an ingredient
        
        Args:
            ingredient_name: Name of ingredient
            
        Returns:
            List of markets sorted by price (cheapest first)
        """
        commodity = self.INGREDIENT_TO_COMMODITY.get(ingredient_name)
        if not commodity:
            return []
        
        prices = self.fetch_mandi_prices(commodity=commodity, state="Karnataka", limit=50)
        
        # Convert and sort by price
        market_prices = []
        for price in prices:
            modal_price = float(price.get('modal_price', 0))
            if modal_price > 0:
                market_prices.append({
                    'market': price.get('market'),
                    'district': price.get('district'),
                    'price_per_kg': modal_price / 100,  # Convert from quintal to kg
                    'min_price_per_kg': float(price.get('min_price', 0)) / 100,
                    'max_price_per_kg': float(price.get('max_price', 0)) / 100,
                    'arrival_date': price.get('arrival_date')
                })
        
        return sorted(market_prices, key=lambda x: x['price_per_kg'])
    
    def compare_prices_across_markets(self, ingredients: List[str]) -> Dict:
        """
        Compare prices of multiple ingredients across markets
        
        Args:
            ingredients: List of ingredient names
            
        Returns:
            Comparison data
        """
        comparison = {}
        
        for ingredient in ingredients:
            markets = self.get_cheapest_markets(ingredient)
            if markets:
                comparison[ingredient] = {
                    'cheapest_market': markets[0] if markets else None,
                    'expensive_market': markets[-1] if markets else None,
                    'price_range': {
                        'min': markets[0]['price_per_kg'] if markets else 0,
                        'max': markets[-1]['price_per_kg'] if markets else 0
                    },
                    'all_markets': markets[:5]  # Top 5 cheapest
                }
        
        return comparison


# Flask routes for mandi prices
def register_mandi_routes(app):
    """Register Flask routes for mandi price API"""
    from flask import jsonify, request
    
    mandi_api = MandiPriceAPI()
    
    @app.route('/api/mandi-prices')
    def api_mandi_prices():
        """Get mandi prices for commodities"""
        commodity = request.args.get('commodity')
        state = request.args.get('state', 'Karnataka')
        limit = int(request.args.get('limit', 50))
        
        prices = mandi_api.fetch_mandi_prices(commodity, state, limit)
        return jsonify({
            'success': True,
            'count': len(prices),
            'prices': prices
        })
    
    @app.route('/api/ingredient-price/<ingredient_name>')
    def api_ingredient_price(ingredient_name):
        """Get current price for an ingredient"""
        market = request.args.get('market', 'Hubli')
        price_info = mandi_api.get_ingredient_price(ingredient_name, market)
        
        if price_info:
            return jsonify({'success': True, 'price': price_info})
        return jsonify({'success': False, 'error': 'Price not found'}), 404
    
    @app.route('/api/update-mandi-prices', methods=['POST'])
    def api_update_mandi_prices():
        """Update all ingredient prices from mandi data"""
        market = request.json.get('market', 'Hubli') if request.json else 'Hubli'
        result = mandi_api.update_all_ingredient_prices(market)
        return jsonify({'success': True, 'result': result})
    
    @app.route('/api/price-trends/<ingredient_name>')
    def api_price_trends(ingredient_name):
        """Get price trends for an ingredient"""
        days = int(request.args.get('days', 30))
        trends = mandi_api.get_price_trends(ingredient_name, days)
        return jsonify({'success': True, 'trends': trends})
    
    @app.route('/api/cheapest-markets/<ingredient_name>')
    def api_cheapest_markets(ingredient_name):
        """Get cheapest markets for an ingredient"""
        markets = mandi_api.get_cheapest_markets(ingredient_name)
        return jsonify({'success': True, 'markets': markets})
    
    @app.route('/api/compare-market-prices', methods=['POST'])
    def api_compare_market_prices():
        """Compare prices of ingredients across markets"""
        ingredients = request.json.get('ingredients', [])
        comparison = mandi_api.compare_prices_across_markets(ingredients)
        return jsonify({'success': True, 'comparison': comparison})


# Standalone test
if __name__ == "__main__":
    print("Testing Mandi Price API...")
    api = MandiPriceAPI()
    
    # Test fetching prices
    print("\n1. Fetching Karnataka mandi prices...")
    prices = api.fetch_mandi_prices(state="Karnataka", limit=10)
    print(f"   Found {len(prices)} price records")
    
    if prices:
        print(f"   Sample: {prices[0]}")
    
    # Test ingredient price
    print("\n2. Getting Rice price in Hubli...")
    rice_price = api.get_ingredient_price("Rice", "Hubli")
    if rice_price:
        print(f"   Rice: ₹{rice_price['price_per_kg']:.2f}/kg at {rice_price['market']}")
    
    # Test cheapest markets
    print("\n3. Finding cheapest markets for Tomato...")
    markets = api.get_cheapest_markets("Tomato")
    for m in markets[:3]:
        print(f"   {m['market']}: ₹{m['price_per_kg']:.2f}/kg")
    
    print("\n✅ Mandi Price API ready!")
