"""
Comprehensive Feature Test for AI Nutrition Advisor
Tests all 60+ features to ensure they're working
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

class FeatureTester:
    def __init__(self):
        self.results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'details': []
        }
    
    def test_feature(self, name, url, method='GET', data=None, expected_status=200):
        """Test a single feature"""
        self.results['total'] += 1
        try:
            if method == 'GET':
                response = requests.get(f"{BASE_URL}{url}", timeout=10)
            elif method == 'POST':
                response = requests.post(f"{BASE_URL}{url}", json=data, timeout=10)
            
            if response.status_code == expected_status:
                self.results['passed'] += 1
                self.results['details'].append({
                    'name': name,
                    'status': 'PASS',
                    'url': url,
                    'code': response.status_code
                })
                print(f"✅ {name}")
                return True
            else:
                self.results['failed'] += 1
                self.results['details'].append({
                    'name': name,
                    'status': 'FAIL',
                    'url': url,
                    'code': response.status_code,
                    'expected': expected_status
                })
                print(f"❌ {name} (Expected {expected_status}, got {response.status_code})")
                return False
        except Exception as e:
            self.results['failed'] += 1
            self.results['details'].append({
                'name': name,
                'status': 'ERROR',
                'url': url,
                'error': str(e)
            })
            print(f"❌ {name} (Error: {str(e)[:50]})")
            return False
    
    def run_all_tests(self):
        """Run all feature tests"""
        print("\n" + "="*80)
        print("🧪 COMPREHENSIVE FEATURE TEST - AI NUTRITION ADVISOR")
        print("="*80 + "\n")
        
        # Core Pages
        print("📄 CORE PAGES:")
        self.test_feature("Home Page", "/")
        self.test_feature("Analytics Dashboard", "/analytics")
        self.test_feature("About Page", "/about")
        self.test_feature("Health Info", "/health-info")
        
        # Meal Planning Features
        print("\n🍽️ MEAL PLANNING:")
        self.test_feature("Meal Planning Page", "/meal-planning")
        self.test_feature("Generate Meal Plan API", "/api/generate-plan", method='POST', 
                         data={'num_children': 20, 'budget': 2000, 'dietary_restrictions': []})
        self.test_feature("Export CSV", "/api/export-csv")
        self.test_feature("Export PDF", "/api/export-pdf")
        self.test_feature("Export JSON", "/api/export-json")
        
        # Immunization Features
        print("\n💉 IMMUNIZATION:")
        self.test_feature("Immunization Page", "/immunisation")
        self.test_feature("WHO Vaccines Info", "/who-vaccines")
        self.test_feature("WHO Vaccine API", "/api/who-vaccine-info")
        self.test_feature("WHO Disease Info API", "/api/who-disease-info")
        
        # Growth Tracking
        print("\n📊 GROWTH TRACKING:")
        self.test_feature("Growth Tracking Page", "/growth-tracking")
        self.test_feature("Get Growth Data", "/api/growth-data/1")
        
        # Nutrition Lookup
        print("\n🔍 NUTRITION LOOKUP:")
        self.test_feature("Nutrition Lookup Page", "/nutrition-lookup")
        self.test_feature("USDA Search API", "/api/usda-search")
        self.test_feature("USDA Compare API", "/api/usda-compare")
        
        # Chatbot Features
        print("\n💬 CHATBOT:")
        self.test_feature("Chatbot Page", "/chatbot")
        self.test_feature("Chatbot API", "/api/chatbot", method='POST',
                         data={'message': 'Hello', 'child_id': 1})
        
        # Village Economy
        print("\n🏘️ VILLAGE ECONOMY:")
        self.test_feature("Village Economy Page", "/village-economy")
        self.test_feature("Economy Score API", "/api/economy-score")
        self.test_feature("Cheapest Foods API", "/api/cheapest-foods")
        self.test_feature("Local Crops API", "/api/local-crops")
        self.test_feature("Spending Analysis API", "/api/spending-analysis")
        self.test_feature("Education Sessions API", "/api/education-sessions")
        self.test_feature("Economy Recommendations API", "/api/economy-recommendations")
        
        # Mandi Prices
        print("\n🏪 MANDI PRICES:")
        self.test_feature("Mandi Prices Page", "/mandi-prices")
        self.test_feature("Mandi Prices API", "/api/mandi-prices")
        self.test_feature("Ingredient Price API", "/api/ingredient-price/rice")
        self.test_feature("Price Trends API", "/api/price-trends/rice")
        self.test_feature("Cheapest Markets API", "/api/cheapest-markets/rice")
        self.test_feature("Compare Market Prices API", "/api/compare-market-prices")
        
        # Child Identity & QR
        print("\n🆔 CHILD IDENTITY:")
        self.test_feature("Child Identity Page", "/child-identity")
        self.test_feature("Child Identity Card Page", "/child-identity-card")
        self.test_feature("QR Scanner Page", "/child-identity-scanner")
        self.test_feature("QR Scan Page", "/qr-scan")
        self.test_feature("Create Identity Card API", "/api/child-identity/create/1")
        self.test_feature("Get Identity Card API", "/api/child-identity/get/1")
        
        # Food Recognition
        print("\n📸 FOOD RECOGNITION:")
        self.test_feature("Food Recognition Page", "/food-recognition")
        self.test_feature("Food Database API", "/api/food-database")
        
        # ML Recommendations
        print("\n🤖 ML RECOMMENDATIONS:")
        self.test_feature("ML Recommendations Page", "/ml-recommendations")
        self.test_feature("ML Train API", "/api/ml/train", method='POST')
        self.test_feature("ML Recommendations API", "/api/ml/recommendations/1")
        self.test_feature("Similar Children API", "/api/ml/similar-children/1")
        self.test_feature("Weekly Variety API", "/api/ml/weekly-variety")
        self.test_feature("Acceptance Prediction API", "/api/ml/acceptance-prediction")
        self.test_feature("Child Profile API", "/api/ml/child-profile/1")
        
        # Malnutrition Prediction
        print("\n⚕️ MALNUTRITION PREDICTION:")
        self.test_feature("Malnutrition Prediction Page", "/malnutrition-prediction")
        self.test_feature("Predict Malnutrition API", "/api/predict-malnutrition/1")
        self.test_feature("Malnutrition Stats API", "/api/malnutrition-stats")
        
        # ASHA Dashboard
        print("\n👩‍⚕️ ASHA DASHBOARD:")
        self.test_feature("ASHA Dashboard Page", "/asha-dashboard")
        self.test_feature("Get Children API", "/api/get-children")
        self.test_feature("Get Child API", "/api/get-child/1")
        self.test_feature("All Vaccinations API", "/api/asha/all-vaccinations/1")
        self.test_feature("Pending Vaccinations API", "/api/asha/pending-vaccinations/1")
        self.test_feature("Nutrition Score API", "/api/asha/nutrition-score/1")
        
        # Village Analytics
        print("\n📈 VILLAGE ANALYTICS:")
        self.test_feature("Village Analytics Page", "/village-analytics")
        
        # Reports
        print("\n📋 REPORTS:")
        self.test_feature("Reports Page", "/reports")
        
        # Legal Cases
        print("\n⚖️ LEGAL CASES:")
        self.test_feature("Legal Cases API", "/api/legal-cases")
        self.test_feature("Legal Cases Search API", "/api/legal-cases/search")
        
        # Child Management
        print("\n👶 CHILD MANAGEMENT:")
        self.test_feature("Add Child API", "/api/add-child", method='POST',
                         data={'name': 'Test Child', 'age_months': 24, 'gender': 'M'})
        
        # Health Check
        print("\n🏥 SYSTEM:")
        self.test_feature("Health Check", "/health")
        
        # Print Summary
        print("\n" + "="*80)
        print("📊 TEST SUMMARY")
        print("="*80)
        print(f"Total Tests: {self.results['total']}")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        print(f"Success Rate: {(self.results['passed']/self.results['total']*100):.1f}%")
        print("="*80)
        
        # Show failed tests
        if self.results['failed'] > 0:
            print("\n❌ FAILED FEATURES:")
            for detail in self.results['details']:
                if detail['status'] in ['FAIL', 'ERROR']:
                    print(f"  • {detail['name']}: {detail.get('error', f'Status {detail.get('code')}')} ({detail['url']})")
        
        return self.results

if __name__ == '__main__':
    tester = FeatureTester()
    results = tester.run_all_tests()
    
    # Save results
    with open('test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📝 Results saved to test_results.json")
