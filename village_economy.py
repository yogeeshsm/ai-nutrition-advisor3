"""
Village Nutrition Economy Analyzer
Tracks local food ecosystem, pricing trends, and nutrition economics
Integrates with data.gov.in Mandi Prices API for real-time prices
"""

from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import json
import os

# Import Mandi Price API for real-time government prices
try:
    from mandi_price_api import MandiPriceAPI
    MANDI_API_AVAILABLE = True
except ImportError:
    MANDI_API_AVAILABLE = False
    print("Warning: Mandi Price API not available. Using local data only.")

def get_connection():
    """Create database connection"""
    return sqlite3.connect('nutrition_advisor.db')

def initialize_economy_tables():
    """Initialize tables for village nutrition economy tracking"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Food price tracking table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredient_name TEXT NOT NULL,
            village TEXT,
            price_per_kg REAL NOT NULL,
            month TEXT NOT NULL,
            year INTEGER NOT NULL,
            source TEXT,
            recorded_date DATE DEFAULT CURRENT_DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Local crops and seasonal availability
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS local_crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop_name TEXT NOT NULL,
            village TEXT,
            season TEXT,
            avg_price_per_kg REAL,
            nutrition_score REAL,
            availability_months TEXT,
            is_locally_grown INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Family spending patterns
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS family_spending (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            family_id TEXT,
            village TEXT,
            month TEXT NOT NULL,
            year INTEGER NOT NULL,
            nutritious_food_spend REAL DEFAULT 0,
            junk_food_spend REAL DEFAULT 0,
            total_food_spend REAL DEFAULT 0,
            notes TEXT,
            recorded_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Nutrition education tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS education_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            village TEXT,
            session_date DATE NOT NULL,
            topic TEXT,
            attendees INTEGER DEFAULT 0,
            asha_worker TEXT,
            key_learnings TEXT,
            follow_up_needed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Village statistics
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS village_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            village TEXT NOT NULL,
            total_families INTEGER DEFAULT 0,
            total_children INTEGER DEFAULT 0,
            avg_monthly_income REAL,
            food_budget_percentage REAL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Village Nutrition Economy tables initialized!")


class VillageEconomyAnalyzer:
    """
    Class-based wrapper for village economy analysis functions
    Provides clean API for Flask routes
    """
    
    def __init__(self):
        # Initialize tables if needed
        initialize_economy_tables()
    
    def get_economy_score(self, village=None):
        """Get overall nutrition economy score"""
        result = calculate_nutrition_economy_score(village if village else None)
        if result:
            return result
        return {
            'score': 75,  # Default score
            'junk_percentage': 25,
            'total_families_tracked': 0,
            'avg_monthly_spend': 4500
        }
    
    def get_cheapest_nutritious_foods(self, village=None, limit=20):
        """Get cheapest nutritious foods this month"""
        df = get_cheapest_foods_this_month(village if village else None)
        if df.empty:
            # Return sample data if no data available
            return self._get_sample_cheapest_foods()
        return df.to_dict('records')
    
    def get_best_local_crops(self, village=None):
        """Get best local crops available now"""
        df = get_best_local_crops(village if village else None)
        if df.empty:
            return self._get_sample_local_crops()
        return df.to_dict('records')
    
    def analyze_spending_patterns(self, village=None):
        """Analyze spending patterns"""
        df = get_junk_food_spending(village if village else None)
        if df.empty:
            return self._get_sample_spending()
        return df.to_dict('records')
    
    def get_education_sessions(self, village=None):
        """Get education sessions"""
        conn = get_connection()
        query = "SELECT * FROM education_sessions"
        params = []
        if village:
            query += " WHERE village = ?"
            params.append(village)
        query += " ORDER BY session_date DESC LIMIT 10"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        if df.empty:
            return self._get_sample_education_sessions()
        return df.to_dict('records')
    
    def get_recommendations(self, village=None):
        """Get cost-effective recommendations"""
        return get_cost_effective_recommendations(village if village else None)
    
    def add_price_update(self, data):
        """Add a new price update"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO food_prices (ingredient_name, village, price_per_kg, month, year, source)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data.get('ingredient_name'),
                data.get('village'),
                data.get('price_per_kg'),
                datetime.now().strftime('%B'),
                datetime.now().year,
                data.get('source', 'Manual Entry')
            ))
            conn.commit()
            return {'success': True, 'message': 'Price updated successfully'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            conn.close()
    
    def _get_sample_cheapest_foods(self):
        """Return sample data when no real data available"""
        return [
            {'ingredient_name': 'Rice', 'category': 'Grains', 'avg_price': 45.0, 'protein_per_100g': 7.1, 'calories_per_100g': 360, 'nutrition_per_rupee': 2.5},
            {'ingredient_name': 'Ragi', 'category': 'Millets', 'avg_price': 60.0, 'protein_per_100g': 7.3, 'calories_per_100g': 336, 'nutrition_per_rupee': 2.3},
            {'ingredient_name': 'Jowar', 'category': 'Millets', 'avg_price': 50.0, 'protein_per_100g': 10.4, 'calories_per_100g': 349, 'nutrition_per_rupee': 2.6},
            {'ingredient_name': 'Potato', 'category': 'Vegetables', 'avg_price': 25.0, 'protein_per_100g': 2.0, 'calories_per_100g': 77, 'nutrition_per_rupee': 1.8},
            {'ingredient_name': 'Banana', 'category': 'Fruits', 'avg_price': 40.0, 'protein_per_100g': 1.1, 'calories_per_100g': 89, 'nutrition_per_rupee': 1.2},
            {'ingredient_name': 'Moong Dal', 'category': 'Pulses', 'avg_price': 120.0, 'protein_per_100g': 24.0, 'calories_per_100g': 347, 'nutrition_per_rupee': 2.1},
            {'ingredient_name': 'Spinach', 'category': 'Vegetables', 'avg_price': 45.0, 'protein_per_100g': 2.9, 'calories_per_100g': 23, 'nutrition_per_rupee': 3.0},
            {'ingredient_name': 'Tomato', 'category': 'Vegetables', 'avg_price': 35.0, 'protein_per_100g': 0.9, 'calories_per_100g': 18, 'nutrition_per_rupee': 1.5},
        ]
    
    def _get_sample_local_crops(self):
        """Return sample local crops data"""
        return [
            {'crop_name': 'Ragi (Finger Millet)', 'season': 'Winter', 'avg_price_per_kg': 60, 'nutrition_score': 85, 'protein_per_100g': 7.3, 'iron_per_100g': 3.9, 'calcium_per_100g': 344},
            {'crop_name': 'Jowar (Sorghum)', 'season': 'Winter', 'avg_price_per_kg': 50, 'nutrition_score': 80, 'protein_per_100g': 10.4, 'iron_per_100g': 4.1, 'calcium_per_100g': 25},
            {'crop_name': 'Spinach (Palak)', 'season': 'Winter', 'avg_price_per_kg': 45, 'nutrition_score': 90, 'protein_per_100g': 2.9, 'iron_per_100g': 2.7, 'calcium_per_100g': 99},
            {'crop_name': 'Carrot', 'season': 'Winter', 'avg_price_per_kg': 55, 'nutrition_score': 75, 'protein_per_100g': 0.9, 'iron_per_100g': 0.3, 'calcium_per_100g': 33},
        ]
    
    def _get_sample_spending(self):
        """Return sample spending data"""
        current_month = datetime.now().strftime('%B')
        current_year = datetime.now().year
        return [
            {'village': 'Hubballi', 'month': current_month, 'year': current_year, 'families': 25, 'total_nutritious': 87500, 'total_junk': 30000, 'junk_percentage': 25.5},
            {'village': 'Dharwad', 'month': current_month, 'year': current_year, 'families': 20, 'total_nutritious': 76000, 'total_junk': 21000, 'junk_percentage': 21.6},
        ]
    
    def _get_sample_education_sessions(self):
        """Return sample education sessions"""
        return [
            {'village': 'Hubballi', 'session_date': datetime.now().strftime('%Y-%m-%d'), 'topic': 'Cost-effective Nutrition', 'attendees': 25, 'asha_worker': 'Sunita Devi', 'key_learnings': 'Families learned about ragi benefits', 'follow_up_needed': 1},
            {'village': 'Dharwad', 'session_date': datetime.now().strftime('%Y-%m-%d'), 'topic': 'Local Crops Nutrition Value', 'attendees': 30, 'asha_worker': 'Kavita Patil', 'key_learnings': 'Discussed seasonal vegetables', 'follow_up_needed': 0},
        ]


def get_cheapest_foods_this_month(village=None):
    """Get cheapest nutritious foods for current month"""
    conn = get_connection()
    current_month = datetime.now().strftime('%B')
    current_year = datetime.now().year
    
    query = """
        SELECT 
            fp.ingredient_name,
            fp.village,
            AVG(fp.price_per_kg) as avg_price,
            i.calories_per_100g,
            i.protein_per_100g,
            i.category,
            (i.protein_per_100g * 2 + i.fiber_per_100g + i.iron_per_100g) / AVG(fp.price_per_kg) as nutrition_per_rupee
        FROM food_prices fp
        LEFT JOIN ingredients i ON fp.ingredient_name = i.name
        WHERE fp.month = ? AND fp.year = ?
    """
    params = [current_month, current_year]
    
    if village:
        query += " AND fp.village = ?"
        params.append(village)
    
    query += """
        GROUP BY fp.ingredient_name
        ORDER BY nutrition_per_rupee DESC
        LIMIT 20
    """
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_best_local_crops(village=None):
    """Get local crops offering best nutrition value"""
    conn = get_connection()
    current_month = datetime.now().strftime('%B')
    
    query = """
        SELECT 
            lc.crop_name,
            lc.village,
            lc.season,
            lc.avg_price_per_kg,
            lc.nutrition_score,
            lc.availability_months,
            i.protein_per_100g,
            i.calories_per_100g,
            i.fiber_per_100g,
            i.iron_per_100g,
            i.calcium_per_100g
        FROM local_crops lc
        LEFT JOIN ingredients i ON lc.crop_name = i.name
        WHERE lc.availability_months LIKE ?
    """
    params = [f'%{current_month}%']
    
    if village:
        query += " AND lc.village = ?"
        params.append(village)
    
    query += " ORDER BY lc.nutrition_score DESC"
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_junk_food_spending(village=None, months=6):
    """Analyze junk food vs nutritious food spending"""
    conn = get_connection()
    
    query = """
        SELECT 
            village,
            month,
            year,
            SUM(nutritious_food_spend) as total_nutritious,
            SUM(junk_food_spend) as total_junk,
            SUM(total_food_spend) as total_spend,
            COUNT(DISTINCT family_id) as families,
            ROUND(AVG(junk_food_spend * 100.0 / NULLIF(total_food_spend, 0)), 2) as junk_percentage
        FROM family_spending
        WHERE created_at >= date('now', '-' || ? || ' months')
    """
    params = [months]
    
    if village:
        query += " AND village = ?"
        params.append(village)
    
    query += """
        GROUP BY village, month, year
        ORDER BY year DESC, month DESC
    """
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_price_trends(ingredient_name, months=12):
    """Get price trends for a specific ingredient"""
    conn = get_connection()
    
    df = pd.read_sql_query("""
        SELECT 
            month,
            year,
            village,
            AVG(price_per_kg) as avg_price,
            MIN(price_per_kg) as min_price,
            MAX(price_per_kg) as max_price,
            COUNT(*) as records
        FROM food_prices
        WHERE ingredient_name = ?
        AND created_at >= date('now', '-' || ? || ' months')
        GROUP BY month, year, village
        ORDER BY year DESC, month DESC
    """, conn, params=[ingredient_name, months])
    
    conn.close()
    return df

def calculate_nutrition_economy_score(village=None):
    """Calculate overall nutrition economy score for a village"""
    conn = get_connection()
    
    # Get average spending patterns
    spending_df = get_junk_food_spending(village)
    
    if spending_df.empty:
        return None
    
    # Calculate metrics
    avg_junk_percentage = spending_df['junk_percentage'].mean()
    
    # Score: Lower junk food percentage = higher score
    nutrition_economy_score = max(0, 100 - avg_junk_percentage)
    
    return {
        'score': round(nutrition_economy_score, 1),
        'junk_percentage': round(avg_junk_percentage, 1),
        'total_families_tracked': spending_df['families'].sum(),
        'avg_monthly_spend': round(spending_df['total_spend'].mean(), 2)
    }

def get_cost_effective_recommendations(village=None, budget=1000):
    """Get cost-effective nutrition recommendations"""
    cheapest_foods = get_cheapest_foods_this_month(village)
    local_crops = get_best_local_crops(village)
    
    recommendations = []
    
    # Recommend cheapest nutritious foods
    if not cheapest_foods.empty:
        top_5 = cheapest_foods.head(5)
        for _, food in top_5.iterrows():
            recommendations.append({
                'type': 'cost_effective',
                'food': food['ingredient_name'],
                'price': food['avg_price'],
                'reason': f"Best nutrition per rupee: ₹{food['avg_price']}/kg with {food['protein_per_100g']}g protein",
                'category': food['category']
            })
    
    # Recommend seasonal local crops
    if not local_crops.empty:
        top_3 = local_crops.head(3)
        for _, crop in top_3.iterrows():
            recommendations.append({
                'type': 'seasonal_local',
                'food': crop['crop_name'],
                'price': crop['avg_price_per_kg'],
                'reason': f"Locally available this month with nutrition score: {crop['nutrition_score']}",
                'season': crop['season']
            })
    
    return recommendations

def add_sample_economy_data():
    """Add sample data for demonstration"""
    conn = get_connection()
    cursor = conn.cursor()
    
    current_month = datetime.now().strftime('%B')
    current_year = datetime.now().year
    
    # First, try to fetch real prices from Mandi API
    if MANDI_API_AVAILABLE:
        try:
            mandi_api = MandiPriceAPI()
            print("🔄 Fetching real-time mandi prices from data.gov.in...")
            
            # Fetch prices for key ingredients
            ingredients_to_fetch = ['Rice', 'Wheat', 'Potato', 'Tomato', 'Onion', 'Banana', 
                                   'Jowar', 'Ragi', 'Moong Dal', 'Spinach', 'Carrot']
            
            for ingredient in ingredients_to_fetch:
                price_info = mandi_api.get_ingredient_price(ingredient, "Hubli")
                if price_info and price_info['price_per_kg'] > 0:
                    cursor.execute("""
                        INSERT OR REPLACE INTO food_prices 
                        (ingredient_name, village, price_per_kg, month, year, source)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        ingredient, 
                        'Hubballi', 
                        price_info['price_per_kg'],
                        current_month,
                        current_year,
                        f"data.gov.in - {price_info.get('market', 'Mandi')}"
                    ))
                    print(f"  ✅ {ingredient}: ₹{price_info['price_per_kg']:.2f}/kg (from {price_info.get('market')})")
            
            conn.commit()
            print("✅ Real mandi prices fetched and saved!")
            
        except Exception as e:
            print(f"⚠️ Error fetching mandi prices: {e}")
            print("   Using sample data instead...")
            _add_sample_prices(cursor, current_month, current_year)
    else:
        _add_sample_prices(cursor, current_month, current_year)
    
    # Add other sample data (local crops, spending, etc.)
    _add_other_sample_data(cursor, current_month, current_year)
    
    conn.commit()
    conn.close()
    print("✅ Sample economy data added!")

def _add_sample_prices(cursor, current_month, current_year):
    """Add fallback sample prices when API is unavailable"""
    sample_prices = [
        ('Rice', 'Hubballi', 45, current_month, current_year, 'Market Survey'),
        ('Wheat Flour (Atta)', 'Hubballi', 35, current_month, current_year, 'Market Survey'),
        ('Moong Dal', 'Hubballi', 120, current_month, current_year, 'Market Survey'),
        ('Potato', 'Hubballi', 25, current_month, current_year, 'Market Survey'),
        ('Tomato', 'Hubballi', 35, current_month, current_year, 'Market Survey'),
        ('Banana', 'Hubballi', 40, current_month, current_year, 'Market Survey'),
        ('Milk', 'Hubballi', 55, current_month, current_year, 'Dairy'),
        ('Spinach (Palak)', 'Hubballi', 45, current_month, current_year, 'Market Survey'),
        ('Ragi (Finger Millet)', 'Dharwad', 60, current_month, current_year, 'Local Farm'),
        ('Jowar (Sorghum)', 'Dharwad', 50, current_month, current_year, 'Local Farm'),
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO food_prices (ingredient_name, village, price_per_kg, month, year, source)
        VALUES (?, ?, ?, ?, ?, ?)
    """, sample_prices)

def _add_other_sample_data(cursor, current_month, current_year):
    """Add sample local crops, spending, education sessions data"""
    
    # Sample local crops
    sample_crops = [
        ('Ragi (Finger Millet)', 'Dharwad', 'Winter', 60, 85, 'November,December,January,February', 1),
        ('Jowar (Sorghum)', 'Hubballi', 'Winter', 50, 80, 'November,December,January', 1),
        ('Tomato', 'Hubballi', 'All Year', 35, 70, 'January,February,March,April,May,June,July,August,September,October,November,December', 1),
        ('Spinach (Palak)', 'Dharwad', 'Winter', 45, 90, 'October,November,December,January,February', 1),
    ]
    
    cursor.executemany("""
        INSERT INTO local_crops (crop_name, village, season, avg_price_per_kg, nutrition_score, availability_months, is_locally_grown)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, sample_crops)
    
    # Sample family spending
    sample_spending = [
        ('FAM001', 'Hubballi', current_month, current_year, 3500, 1200, 4700, 'ASHA Worker Survey'),
        ('FAM002', 'Hubballi', current_month, current_year, 4000, 800, 4800, 'ASHA Worker Survey'),
        ('FAM003', 'Dharwad', current_month, current_year, 3800, 1500, 5300, 'ASHA Worker Survey'),
        ('FAM004', 'Dharwad', current_month, current_year, 4200, 600, 4800, 'ASHA Worker Survey'),
    ]
    
    cursor.executemany("""
        INSERT INTO family_spending (family_id, village, month, year, nutritious_food_spend, junk_food_spend, total_food_spend, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_spending)
    
    # Sample education sessions
    sample_sessions = [
        ('Hubballi', datetime.now().date(), 'Cost-effective Nutrition', 25, 'Sunita Devi', 'Families learned about ragi benefits', 1),
        ('Dharwad', datetime.now().date(), 'Local Crops Nutrition Value', 30, 'Kavita Patil', 'Discussed seasonal vegetables', 0),
    ]
    
    cursor.executemany("""
        INSERT INTO education_sessions (village, session_date, topic, attendees, asha_worker, key_learnings, follow_up_needed)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, sample_sessions)
    
    # Village stats
    sample_stats = [
        ('Hubballi', 150, 380, 18000, 45),
        ('Dharwad', 120, 310, 16500, 42),
    ]
    
    cursor.executemany("""
        INSERT INTO village_stats (village, total_families, total_children, avg_monthly_income, food_budget_percentage)
        VALUES (?, ?, ?, ?, ?)
    """, sample_stats)

def sync_mandi_prices_to_economy():
    """
    Sync real-time mandi prices from data.gov.in to village economy database
    Call this periodically to update prices
    """
    if not MANDI_API_AVAILABLE:
        print("⚠️ Mandi Price API not available")
        return {'success': False, 'error': 'API not available'}
    
    conn = get_connection()
    cursor = conn.cursor()
    
    current_month = datetime.now().strftime('%B')
    current_year = datetime.now().year
    
    try:
        mandi_api = MandiPriceAPI()
        updated = []
        failed = []
        
        # Fetch all Karnataka mandi prices
        prices = mandi_api.fetch_mandi_prices(state="Karnataka", limit=200)
        
        for price in prices:
            commodity = price.get('commodity', '')
            market = price.get('market', 'Unknown')
            modal_price = float(price.get('modal_price', 0))
            
            if modal_price > 0:
                # Convert from Rs/Quintal to Rs/kg
                price_per_kg = modal_price / 100
                
                # Map commodity to our ingredient name
                ingredient_name = _map_commodity_to_ingredient(commodity)
                if ingredient_name:
                    cursor.execute("""
                        INSERT OR REPLACE INTO food_prices 
                        (ingredient_name, village, price_per_kg, month, year, source)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        ingredient_name,
                        market,
                        price_per_kg,
                        current_month,
                        current_year,
                        'data.gov.in'
                    ))
                    updated.append({'ingredient': ingredient_name, 'price': price_per_kg, 'market': market})
        
        conn.commit()
        print(f"✅ Synced {len(updated)} prices from mandi API")
        
        return {
            'success': True,
            'updated_count': len(updated),
            'updated': updated[:20]  # Return first 20 for display
        }
        
    except Exception as e:
        print(f"❌ Error syncing mandi prices: {e}")
        return {'success': False, 'error': str(e)}
    finally:
        conn.close()

def _map_commodity_to_ingredient(commodity):
    """Map mandi commodity name to our ingredient name"""
    # Reverse mapping from MandiPriceAPI
    commodity_to_ingredient = {
        'Rice': 'Rice',
        'Wheat': 'Wheat',
        'Potato': 'Potato',
        'Tomato': 'Tomato',
        'Onion': 'Onion',
        'Banana': 'Banana',
        'Jowar(Sorghum)': 'Jowar',
        'Bajra(Pearl Millet)': 'Bajra',
        'Ragi (Finger Millet)': 'Ragi',
        'Green Gram Dal (Moong Dal)': 'Moong Dal',
        'Arhar (Tur/Red Gram)(Whole)': 'Toor Dal',
        'Bengal Gram(Gram)(Whole)': 'Chickpeas',
        'Spinach': 'Spinach',
        'Carrot': 'Carrot',
        'Cabbage': 'Cabbage',
        'Cauliflower': 'Cauliflower',
        'Brinjal': 'Brinjal',
        'Beans': 'Beans',
        'Groundnut': 'Groundnut',
        'Coconut': 'Coconut',
        'Garlic': 'Garlic',
        'Ginger(Green)': 'Ginger',
        'Green Chilli': 'Green Chilli',
        'Lemon': 'Lemon',
        'Apple': 'Apple',
        'Orange': 'Orange',
        'Mango': 'Mango',
        'Papaya': 'Papaya',
        'Guava': 'Guava',
        'Grapes': 'Grapes',
    }
    
    return commodity_to_ingredient.get(commodity)

# Initialize tables when module is imported
if __name__ == "__main__":
    initialize_economy_tables()
    add_sample_economy_data()
    
    # Try syncing real mandi prices
    print("\n🔄 Syncing real-time mandi prices...")
    sync_result = sync_mandi_prices_to_economy()
    if sync_result['success']:
        print(f"   Updated {sync_result['updated_count']} prices")
    
    print("\n📊 Testing Village Nutrition Economy Analyzer...")
    
    print("\n🏆 Cheapest Foods This Month:")
    print(get_cheapest_foods_this_month('Hubballi'))
    
    print("\n🌾 Best Local Crops:")
    print(get_best_local_crops('Hubballi'))
    
    print("\n🍔 Junk Food Spending Analysis:")
    print(get_junk_food_spending('Hubballi'))
    
    print("\n💯 Nutrition Economy Score:")
    print(calculate_nutrition_economy_score('Hubballi'))
    
    print("\n💡 Cost-Effective Recommendations:")
    recommendations = get_cost_effective_recommendations('Hubballi', 1000)
    for rec in recommendations:
        print(f"  {rec['food']}: {rec['reason']}")
