"""
Flask-based AI Nutrition Advisor
Modern web application with beautiful UI for generating meal plans
"""

from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
import json
from datetime import datetime
import io
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import custom modules
import database as db
import meal_optimizer as mo
from utils import export_to_pdf, get_food_emoji, format_currency
from usda_api import get_usda_api
from who_immunization import who_api

# Try to import optional modules
try:
    # Use Gemini chatbot (stable with Python 3.13)
    from gemini_chatbot import get_chatbot
    CHATBOT_AVAILABLE = True
except (Exception, KeyboardInterrupt, SystemExit) as e:
    print(f"WARNING: Chatbot not available: {e}")
    CHATBOT_AVAILABLE = False
    def get_chatbot():
        return None

try:
    from translator import get_translation_service, LANGUAGES, t
    TRANSLATOR_AVAILABLE = True
except (Exception, KeyboardInterrupt, SystemExit) as e:
    print(f"WARNING: Translator not available: {e}")
    TRANSLATOR_AVAILABLE = False
    LANGUAGES = {'en': 'English'}
    def t(key, lang='en'):
        return key
    def get_translation_service():
        return None

try:
    from mandi_price_api import register_mandi_routes, MandiPriceAPI
    MANDI_AVAILABLE = True
except (Exception, KeyboardInterrupt, SystemExit) as e:
    print(f"WARNING: Mandi API not available: {e}")
    MANDI_AVAILABLE = False
    def register_mandi_routes(app):
        pass
    class MandiPriceAPI:
        pass

try:
    from child_identity_qr import register_child_identity_routes
    CHILD_ID_AVAILABLE = True
except (Exception, KeyboardInterrupt, SystemExit) as e:
    print(f"WARNING: Child Identity QR not available: {e}")
    CHILD_ID_AVAILABLE = False
    def register_child_identity_routes(app):
        pass

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'nutrition-advisor-secret-key-2025')

# Register Mandi Price API routes
register_mandi_routes(app)

# Register Child Identity Card routes
register_child_identity_routes(app)

# Initialize translation service
translation_service = get_translation_service()

# Initialize chatbot with provider from environment
if CHATBOT_AVAILABLE:
    try:
        chatbot = get_chatbot()
        print(f"✅ Chatbot initialized with gemini")
    except Exception as e:
        print(f"⚠️  Chatbot error: {e}")
        chatbot = None
else:
    chatbot = None

# Make translation functions available in templates
@app.context_processor
def inject_translation():
    """Inject translation functions into all templates"""
    lang = session.get('language', 'en')
    if translation_service:
        return dict(
            t=lambda key: translation_service.get_translation(key, lang),
            current_language=lang,
            languages=LANGUAGES,
            translate=lambda text: translation_service.translate(text, lang) if lang != 'en' else text
        )
    else:
        # Fallback when translation service is not available
        return dict(
            t=lambda key: key,
            current_language='en',
            languages={'en': 'English'},
            translate=lambda text: text
        )

# Initialize database on startup
db.initialize_database()

@app.route('/health')
def health_check():
    """Health check endpoint for Render"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Nutrition Advisor',
        'features': '60+',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/')
def index():
    """Home page - Meal Planner"""
    # Get ingredients organized by category
    ingredients_df = db.get_all_ingredients()
    ingredients_by_category = db.get_ingredients_by_category()
    
    # Convert to list of dicts for easier template rendering
    ingredients_data = []
    for category, ingredients in ingredients_by_category.items():
        category_items = []
        for ing_name in ingredients:
            ing = ingredients_df[ingredients_df['name'] == ing_name].iloc[0]
            # Determine unit based on serving size
            serving_size = ing['serving_size_g']
            
            # Determine unit and display cost based on serving size
            if ing_name == 'Milk':
                unit = '1000ml'
                display_cost = ing['cost_per_kg']  # Already per 1000ml
                display_serving = 1000
            elif ing_name == 'Curd (Yogurt)':
                unit = '50gm'
                display_cost = ing['cost_per_kg'] / 20  # Convert to per 50gm
                display_serving = 50
            elif ing_name == 'Paneer':
                unit = '200gm'
                display_cost = ing['cost_per_kg'] / 5  # Convert to per 200gm
                display_serving = 200
            elif category == 'Dairy':
                unit = 'ml'
                display_cost = ing['cost_per_kg']
                display_serving = serving_size
            elif category == 'Leafy Vegetables':
                unit = ''  # No unit for leafy vegetables
                display_cost = ing['cost_per_kg']
                display_serving = serving_size
            elif ing_name == 'Eggs':
                unit = ''  # No unit for eggs
                display_cost = ing['cost_per_kg']
                display_serving = serving_size
            elif serving_size >= 1000:
                unit = 'kg'
                display_cost = ing['cost_per_kg']
                display_serving = serving_size
            else:
                unit = 'kg'
                display_cost = ing['cost_per_kg']
                display_serving = serving_size
            
            category_items.append({
                'name': ing['name'],
                'cost': display_cost,
                'calories': ing['calories_per_100g'],
                'emoji': get_food_emoji(category, ing_name),
                'unit': unit,
                'serving_size': display_serving
            })
        ingredients_data.append({
            'category': category,
            'emoji': get_food_emoji(category),
            'ingredients': category_items  # Changed from 'items' to 'ingredients'
        })
    
    return render_template('index.html', ingredients=ingredients_data)

@app.route('/api/generate-plan', methods=['POST'])
def generate_plan():
    """API endpoint to generate meal plan"""
    try:
        data = request.get_json()
        
        # Extract parameters
        num_children = int(data.get('num_children', 20))
        budget = float(data.get('budget', 2000))
        age_group = data.get('age_group', '3-6 years')
        selected_ingredients = data.get('ingredients', [])
        
        if not selected_ingredients:
            return jsonify({
                'success': False,
                'error': 'Please select at least 5 ingredients'
            }), 400
        
        # Get ingredients dataframe
        ingredients_df = db.get_all_ingredients()
        
        # Create optimizer
        optimizer = mo.MealOptimizer(
            ingredients_df=ingredients_df,
            budget=budget,
            num_children=num_children,
            age_group=age_group
        )
        
        # Generate meal plan
        meal_plan = optimizer.generate_meal_plan(selected_ingredients)
        
        # Save to database
        plan_data = json.dumps({
            'weekly_plan': meal_plan['weekly_plan'],
            'selected_ingredients': selected_ingredients
        }, default=str)
        
        plan_id = db.save_meal_plan(
            plan_name=f"Plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            budget=budget,
            num_children=num_children,
            age_group=age_group,
            total_cost=meal_plan['total_cost'],
            nutrition_score=meal_plan['nutrition_score'],
            plan_data=plan_data
        )
        
        # Store in session for later retrieval
        session['current_plan'] = meal_plan
        session['plan_id'] = plan_id
        session['num_children'] = num_children
        session['budget'] = budget
        
        # Format response
        response_data = {
            'success': True,
            'plan_id': plan_id,
            'total_cost': round(meal_plan['total_cost'], 2),
            'nutrition_score': meal_plan['nutrition_score'],
            'weekly_nutrition': meal_plan['weekly_nutrition'],
            'daily_requirements': meal_plan['daily_requirements'],
            'weekly_plan': format_weekly_plan(meal_plan['weekly_plan']),
            'summary': get_plan_summary(meal_plan, num_children, budget)
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export-csv')
def export_csv():
    """Export meal plan as CSV"""
    try:
        meal_plan = session.get('current_plan')
        if not meal_plan:
            return jsonify({'error': 'No meal plan found'}), 404
        
        # Format as dataframe
        formatted_df = mo.format_meal_plan_for_display(meal_plan)
        
        # Create CSV in memory
        output = io.StringIO()
        formatted_df.to_csv(output, index=False)
        output.seek(0)
        
        # Convert to bytes
        mem = io.BytesIO()
        mem.write(output.getvalue().encode())
        mem.seek(0)
        
        return send_file(
            mem,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'meal_plan_{datetime.now().strftime("%Y%m%d")}.csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-pdf')
def export_pdf():
    """Export meal plan as PDF"""
    try:
        meal_plan = session.get('current_plan')
        num_children = session.get('num_children', 20)
        budget = session.get('budget', 2000)
        
        if not meal_plan:
            return jsonify({'error': 'No meal plan found'}), 404
        
        # Generate PDF
        pdf_data = export_to_pdf(meal_plan, num_children, budget)
        
        # Create file in memory
        mem = io.BytesIO(pdf_data)
        mem.seek(0)
        
        return send_file(
            mem,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'meal_plan_{datetime.now().strftime("%Y%m%d")}.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-json')
def export_json():
    """Export meal plan as JSON"""
    try:
        meal_plan = session.get('current_plan')
        if not meal_plan:
            return jsonify({'error': 'No meal plan found'}), 404
        
        # Convert to JSON string
        json_str = json.dumps(meal_plan, indent=2, default=str)
        
        # Create file in memory
        mem = io.BytesIO(json_str.encode())
        mem.seek(0)
        
        return send_file(
            mem,
            mimetype='application/json',
            as_attachment=True,
            download_name=f'meal_plan_{datetime.now().strftime("%Y%m%d")}.json'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analytics')
def analytics():
    """Analytics dashboard page"""
    # Get analytics data
    plans_df, effectiveness_df = db.get_analytics_data()
    recent_plans = db.get_recent_meal_plans(20)
    
    # Calculate summary metrics
    summary = {
        'total_plans': len(recent_plans),
        'avg_score': round(recent_plans['nutrition_score'].mean(), 1) if len(recent_plans) > 0 else 0,
        'avg_cost': round(recent_plans['total_cost'].mean(), 2) if len(recent_plans) > 0 else 0,
        'avg_children': round(recent_plans['num_children'].mean(), 0) if len(recent_plans) > 0 else 0
    }
    
    # Format for charts
    budget_vs_score = effectiveness_df.to_dict('records') if len(effectiveness_df) > 0 else []
    age_group_stats = plans_df.to_dict('records') if len(plans_df) > 0 else []
    recent_plans_list = recent_plans.to_dict('records') if len(recent_plans) > 0 else []
    
    return render_template(
        'analytics.html',
        summary=summary,
        budget_vs_score=budget_vs_score,
        age_group_stats=age_group_stats,
        recent_plans=recent_plans_list
    )

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/set_language/<lang>')
def set_language(lang):
    """Set user's preferred language"""
    # Validate language code
    if lang in LANGUAGES:
        session['language'] = lang
        session.permanent = True  # Make session permanent
    
    # Redirect back to the page they came from or home
    return redirect(request.referrer or url_for('index'))

def format_weekly_plan(weekly_plan):
    """Format weekly plan for frontend display"""
    formatted = {}
    for day, day_data in weekly_plan.items():
        formatted[day] = {
            'meals': {},
            'total_cost': round(day_data['total_cost'], 2),
            'total_nutrition': day_data['total_nutrition']
        }
        
        for meal_type, meal_data in day_data['meals'].items():
            formatted[day]['meals'][meal_type] = {
                'items': meal_data['items'],
                'nutrition': meal_data['nutrition'],
                'cost': round(meal_data['cost'], 2)
            }
    
    return formatted

def get_plan_summary(meal_plan, num_children, budget):
    """Get summary statistics"""
    return {
        'total_cost': round(meal_plan['total_cost'], 2),
        'budget': budget,
        'budget_percentage': round((meal_plan['total_cost'] / budget) * 100, 1),
        'nutrition_score': meal_plan['nutrition_score'],
        'per_child_week': round(meal_plan['total_cost'] / num_children, 2),
        'per_child_day': round(meal_plan['total_cost'] / (num_children * 7), 2),
        'per_meal': round(meal_plan['total_cost'] / (num_children * 7 * 4), 2),
        'daily_calories': round(meal_plan['weekly_nutrition']['calories'] / 7, 0),
        'daily_protein': round(meal_plan['weekly_nutrition']['protein'] / 7, 1)
    }

@app.route('/health-info')
def health_info():
    """Health Information Page"""
    # Get all health information
    health_data = db.get_health_info_by_category()
    
    # Get unique categories
    categories = health_data['category'].unique().tolist() if not health_data.empty else []
    
    return render_template('health_info.html', 
                         health_data=health_data.to_dict('records'),
                         categories=categories)

@app.route('/api/search-health')
def search_health():
    """API endpoint to search health information"""
    search_term = request.args.get('q', '')
    category = request.args.get('category', '')
    
    if search_term:
        results = db.search_health_info(search_term)
    elif category:
        results = db.get_health_info_by_category(category)
    else:
        results = db.get_health_info_by_category()
    
    return jsonify(results.to_dict('records'))

@app.route('/immunisation')
def immunisation():
    """Immunisation Reminder Page"""
    children = db.get_all_children()
    pending_immunisations = db.get_pending_immunisations()
    
    return render_template('immunisation.html',
                         children=children.to_dict('records'),
                         pending=pending_immunisations.to_dict('records'))

@app.route('/api/add-child', methods=['POST'])
def api_add_child():
    """API endpoint to add a new child"""
    try:
        data = request.json
        child_id = db.add_child(
            name=data['name'],
            dob=data['dob'],
            gender=data.get('gender', ''),
            parent_name=data.get('parent_name', ''),
            phone=data.get('phone', ''),
            address=data.get('address', ''),
            village=data.get('village', ''),
            health_notes=data.get('health_notes', '')
        )
        return jsonify({'success': True, 'child_id': child_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/add-immunisation', methods=['POST'])
def api_add_immunisation():
    """API endpoint to add immunisation schedule"""
    try:
        data = request.json
        db.add_immunisation(
            child_id=data['child_id'],
            vaccine_name=data['vaccine_name'],
            due_date=data['due_date'],
            notes=data.get('notes', '')
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/mark-immunisation-done', methods=['POST'])
def api_mark_done():
    """API endpoint to mark immunisation as completed"""
    try:
        data = request.json
        db.mark_immunisation_done(
            immunisation_id=data['id'],
            administered_date=data['date'],
            notes=data.get('notes', '')
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/growth-tracking')
def growth_tracking():
    """Growth Tracking Page"""
    children = db.get_all_children()
    return render_template('growth_tracking.html', children=children.to_dict('records'))

@app.route('/api/growth-data/<int:child_id>')
def api_growth_data(child_id):
    """API endpoint to get growth data for a child"""
    try:
        # Get growth history
        history = db.get_child_growth_history(child_id)
        
        # Get latest measurement
        latest = db.get_latest_growth(child_id)
        
        # Get chart data
        chart_df = db.get_growth_chart_data(child_id)
        
        # Calculate WHO Z-scores if latest measurement exists
        who_status = 'No data'
        if latest and len(chart_df) > 0:
            age_months = chart_df.iloc[-1]['age_months']
            gender = chart_df.iloc[-1]['gender']
            z_scores = db.calculate_who_z_scores(
                age_months, 
                latest['weight_kg'], 
                latest['height_cm'], 
                gender
            )
            who_status = z_scores['status']
        
        # Format chart data
        chart_data = {
            'dates': chart_df['measurement_date'].dt.strftime('%Y-%m-%d').tolist() if len(chart_df) > 0 else [],
            'weights': chart_df['weight_kg'].tolist() if len(chart_df) > 0 else [],
            'heights': chart_df['height_cm'].tolist() if len(chart_df) > 0 else [],
            'bmis': chart_df['bmi'].fillna(0).tolist() if len(chart_df) > 0 else [],
            'weight_velocity': [],
            'height_velocity': []
        }
        
        # Calculate growth velocity (gain per month)
        if len(chart_df) > 1:
            for i in range(1, len(chart_df)):
                days_diff = (chart_df.iloc[i]['measurement_date'] - chart_df.iloc[i-1]['measurement_date']).days
                months_diff = days_diff / 30.44 if days_diff > 0 else 1
                
                weight_gain = (chart_df.iloc[i]['weight_kg'] - chart_df.iloc[i-1]['weight_kg']) / months_diff
                height_gain = (chart_df.iloc[i]['height_cm'] - chart_df.iloc[i-1]['height_cm']) / months_diff
                
                chart_data['weight_velocity'].append(round(weight_gain, 2))
                chart_data['height_velocity'].append(round(height_gain, 2))
        
        return jsonify({
            'success': True,
            'latest': latest,
            'history': history.to_dict('records'),
            'chart_data': chart_data,
            'who_status': who_status
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/add-growth-measurement', methods=['POST'])
def api_add_growth_measurement():
    """API endpoint to add a new growth measurement"""
    try:
        data = request.json
        measurement_id = db.add_growth_measurement(
            child_id=data['child_id'],
            measurement_date=data['measurement_date'],
            weight_kg=data['weight_kg'],
            height_cm=data['height_cm'],
            head_circumference_cm=data.get('head_circumference_cm'),
            muac_cm=data.get('muac_cm'),
            notes=data.get('notes', ''),
            measured_by=data.get('measured_by', '')
        )
        return jsonify({'success': True, 'measurement_id': measurement_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/nutrition-lookup')
def nutrition_lookup():
    """USDA Nutrition Lookup Page"""
    return render_template('nutrition_lookup.html')

@app.route('/api/usda-search')
def api_usda_search():
    """API endpoint to search USDA food database"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    
    api = get_usda_api()
    if not api:
        return jsonify({'error': 'USDA API not configured. Please set USDA_API_KEY environment variable.'}), 500
    
    results = api.search_foods(query, page_size=10)
    return jsonify(results)

@app.route('/api/usda-details/<int:fdc_id>')
def api_usda_details(fdc_id):
    """API endpoint to get detailed nutrition info"""
    api = get_usda_api()
    if not api:
        return jsonify({'error': 'USDA API not configured'}), 500
    
    details = api.get_nutrition_summary(fdc_id)
    if not details:
        return jsonify({'error': 'Food not found'}), 404
    
    return jsonify(details)

@app.route('/api/usda-compare', methods=['POST'])
def api_usda_compare():
    """API endpoint to compare multiple foods"""
    data = request.json
    food_names = data.get('foods', [])
    
    if not food_names:
        return jsonify({'error': 'No foods provided'}), 400
    
    api = get_usda_api()
    if not api:
        return jsonify({'error': 'USDA API not configured'}), 500
    
    comparison = api.compare_foods(food_names)
    return jsonify(comparison)

@app.route('/who-vaccines')
def who_vaccines():
    """WHO Vaccination Information Page"""
    schedule = who_api.get_vaccination_schedule()
    coverage = who_api.get_immunization_coverage('India')
    missed_reasons = who_api.get_missed_opportunities()
    
    return render_template('who_vaccines.html',
                         schedule=schedule,
                         coverage=coverage,
                         missed_reasons=missed_reasons)

@app.route('/api/who-vaccine-info')
def api_who_vaccine_info():
    """API endpoint to get vaccine information"""
    vaccine_name = request.args.get('vaccine', '')
    
    if not vaccine_name:
        return jsonify({'error': 'Vaccine name required'}), 400
    
    info = who_api.get_vaccine_info(vaccine_name)
    
    if info:
        return jsonify(info)
    else:
        return jsonify({'error': 'Vaccine not found'}), 404

@app.route('/api/who-disease-info')
def api_who_disease_info():
    """API endpoint to get disease information"""
    disease_name = request.args.get('disease', '')
    
    if not disease_name:
        return jsonify({'error': 'Disease name required'}), 400
    
    info = who_api.get_disease_info(disease_name)
    
    if info:
        return jsonify(info)
    else:
        return jsonify({'error': 'Disease not found'}), 404

@app.route('/api/generate-qr/<int:plan_id>')
def generate_qr(plan_id):
    """Generate QR code for meal plan sharing"""
    import qrcode
    from io import BytesIO
    
    # Create URL for this meal plan
    plan_url = f"{request.url_root}plan/{plan_id}"
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(plan_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to BytesIO
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png', download_name=f'meal_plan_qr_{plan_id}.png')

@app.route('/chatbot')
def chatbot_page():
    """AI Nutrition Chatbot Page"""
    return render_template('chatbot.html')

@app.route('/api/chatbot', methods=['POST'])
def api_chatbot():
    """API endpoint for chatbot conversation"""
    try:
        data = request.json
        user_message = data.get('message', '')
        conversation_history = data.get('history', [])
        
        if not user_message:
            return jsonify({'success': False, 'error': 'No message provided'}), 400
        
        if not chatbot:
            return jsonify({
                'success': False, 
                'error': 'Chatbot not initialized. Please set GEMINI_API_KEY environment variable.'
            }), 500
        
        # Get response from chatbot
        response = chatbot.chat(user_message, conversation_history)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chatbot/meal-advice', methods=['POST'])
def api_chatbot_meal_advice():
    """Get AI advice about a specific meal plan"""
    try:
        data = request.json
        meal_plan_data = data.get('meal_plan', {})
        concern = data.get('concern', 'general advice')
        
        if not chatbot:
            return jsonify({'success': False, 'error': 'Chatbot not available'}), 500
        
        advice = chatbot.get_meal_advice(meal_plan_data, concern)
        
        return jsonify({
            'success': True,
            'advice': advice
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chatbot/suggest-alternatives', methods=['POST'])
def api_chatbot_alternatives():
    """Get AI suggestions for ingredient alternatives"""
    try:
        data = request.json
        ingredient = data.get('ingredient', '')
        reason = data.get('reason', 'general')
        
        if not ingredient:
            return jsonify({'success': False, 'error': 'No ingredient provided'}), 400
        
        if not chatbot:
            return jsonify({'success': False, 'error': 'Chatbot not available'}), 500
        
        suggestions = chatbot.suggest_alternatives(ingredient, reason)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Village Nutrition Economy Routes
@app.route('/village-economy')
def village_economy():
    """Village Nutrition Economy Analyzer dashboard"""
    return render_template('village_economy.html')

@app.route('/api/economy-score')
def api_economy_score():
    """Get nutrition economy score for village"""
    from village_economy import VillageEconomyAnalyzer
    analyzer = VillageEconomyAnalyzer()
    
    village = request.args.get('village', '')
    score_data = analyzer.get_economy_score(village)
    
    return jsonify(score_data)

@app.route('/api/cheapest-foods')
def api_cheapest_foods():
    """Get cheapest nutritious foods this month"""
    from village_economy import VillageEconomyAnalyzer
    analyzer = VillageEconomyAnalyzer()
    
    village = request.args.get('village', '')
    limit = int(request.args.get('limit', 20))
    foods = analyzer.get_cheapest_nutritious_foods(village, limit)
    
    return jsonify(foods)

@app.route('/api/local-crops')
def api_local_crops():
    """Get best local crops available now"""
    from village_economy import VillageEconomyAnalyzer
    analyzer = VillageEconomyAnalyzer()
    
    village = request.args.get('village', '')
    crops = analyzer.get_best_local_crops(village)
    
    return jsonify(crops)

@app.route('/api/spending-analysis')
def api_spending_analysis():
    """Get spending pattern analysis"""
    from village_economy import VillageEconomyAnalyzer
    analyzer = VillageEconomyAnalyzer()
    
    village = request.args.get('village', '')
    analysis = analyzer.analyze_spending_patterns(village)
    
    return jsonify(analysis)

@app.route('/api/education-sessions')
def api_education_sessions():
    """Get nutrition education sessions"""
    from village_economy import VillageEconomyAnalyzer
    analyzer = VillageEconomyAnalyzer()
    
    village = request.args.get('village', '')
    sessions = analyzer.get_education_sessions(village)
    
    return jsonify(sessions)

@app.route('/api/economy-recommendations')
def api_economy_recommendations():
    """Get cost-effective nutrition recommendations"""
    from village_economy import VillageEconomyAnalyzer
    analyzer = VillageEconomyAnalyzer()
    
    village = request.args.get('village', '')
    recommendations = analyzer.get_recommendations(village)
    
    return jsonify(recommendations)

@app.route('/api/add-price-update', methods=['POST'])
def api_add_price_update():
    """Add new ingredient price update"""
    from village_economy import VillageEconomyAnalyzer
    analyzer = VillageEconomyAnalyzer()
    
    data = request.json
    result = analyzer.add_price_update(data)
    
    return jsonify(result)

@app.route('/api/sync-mandi-prices', methods=['POST'])
def api_sync_mandi_prices():
    """Sync real-time mandi prices from data.gov.in API"""
    from village_economy import sync_mandi_prices_to_economy
    result = sync_mandi_prices_to_economy()
    return jsonify(result)

# ===== CHILD IDENTITY CARD API ENDPOINTS =====

@app.route('/api/get-children', methods=['GET'])
def api_get_children():
    """Get all children for Child Identity Card selection"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, date_of_birth, gender, village
            FROM children
            WHERE id != 1
            ORDER BY name ASC
        """)
        
        children = []
        for row in cursor.fetchall():
            # Calculate age
            from datetime import datetime
            dob = datetime.strptime(row[2], '%Y-%m-%d')
            age_years = (datetime.now() - dob).days // 365
            
            # Get latest weight from growth_tracking
            cursor.execute("""
                SELECT weight_kg 
                FROM growth_tracking 
                WHERE child_id = ? 
                ORDER BY measurement_date DESC 
                LIMIT 1
            """, (row[0],))
            
            weight_row = cursor.fetchone()
            weight_kg = weight_row[0] if weight_row else 0.0
            
            children.append({
                'id': row[0],
                'name': row[1],
                'date_of_birth': row[2],
                'gender': row[3],
                'village': row[4] if row[4] else 'N/A',
                'age': age_years,
                'age_years': age_years,
                'weight_kg': weight_kg
            })
        
        conn.close()
        
        return jsonify({'success': True, 'children': children})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/get-child/<int:child_id>', methods=['GET'])
def api_get_child(child_id):
    """Get specific child information"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, date_of_birth, gender, parent_name, 
                   village, address
            FROM children
            WHERE id = ?
        """, (child_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return jsonify({'success': False, 'message': 'Child not found'}), 404
        
        # Calculate age
        from datetime import datetime
        dob = datetime.strptime(row[2], '%Y-%m-%d')
        age = (datetime.now() - dob).days // 365
        
        child = {
            'id': row[0],
            'name': row[1],
            'date_of_birth': row[2],
            'gender': row[3],
            'parent_name': row[4] if row[4] else 'N/A',
            'village': row[5] if row[5] else 'N/A',
            'address': row[6] if row[6] else 'N/A',
            'age': age
        }
        
        return jsonify({'success': True, 'child': child})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ===== ASHA WORKER UPDATE ENDPOINTS =====

@app.route('/api/asha/mark-vaccination/<int:child_id>/<vaccine_name>', methods=['POST'])
def asha_mark_vaccination(child_id, vaccine_name):
    """ASHA worker marks a vaccination as completed"""
    from child_identity_qr import ChildIdentityCard
    
    data = request.json or {}
    child_card = ChildIdentityCard()
    
    result = child_card.mark_vaccination_complete(
        child_id=child_id,
        vaccine_name=vaccine_name,
        notes=data.get('notes', '')
    )
    
    return jsonify(result)

@app.route('/api/asha/update-nutrition/<int:child_id>', methods=['POST'])
def asha_update_nutrition(child_id):
    """ASHA worker updates child's nutrition measurements"""
    from child_identity_qr import ChildIdentityCard
    
    data = request.json
    child_card = ChildIdentityCard()
    
    result = child_card.update_nutrition_measurement(
        child_id=child_id,
        weight_kg=data.get('weight_kg'),
        height_cm=data.get('height_cm'),
        notes=data.get('notes', '')
    )
    
    return jsonify(result)

@app.route('/api/asha/pending-vaccinations/<int:child_id>', methods=['GET'])
def asha_get_pending_vaccinations(child_id):
    """Get pending vaccinations for ASHA worker"""
    from child_identity_qr import ChildIdentityCard
    
    child_card = ChildIdentityCard()
    pending = child_card.get_pending_vaccinations(child_id)
    
    return jsonify({'success': True, 'pending_vaccinations': pending})

@app.route('/api/asha/all-vaccinations/<int:child_id>', methods=['GET'])
def asha_get_all_vaccinations(child_id):
    """Get all vaccinations with status"""
    from child_identity_qr import ChildIdentityCard
    
    child_card = ChildIdentityCard()
    vaccinations = child_card.get_all_vaccinations(child_id)
    
    return jsonify({'success': True, 'vaccinations': vaccinations})

@app.route('/api/asha/nutrition-score/<int:child_id>', methods=['GET'])
def asha_get_nutrition_score(child_id):
    """Calculate nutrition score"""
    from child_identity_qr import ChildIdentityCard
    
    child_card = ChildIdentityCard()
    score = child_card.calculate_nutrition_score(child_id)
    
    return jsonify({'success': True, 'nutrition_score': score})


# ========================================
# FOOD IMAGE RECOGNITION ENDPOINTS
# ========================================

@app.route('/food-recognition')
def food_recognition():
    """Food image recognition page"""
    return render_template('food_recognition.html')

@app.route('/api/analyze-food-image', methods=['POST'])
def analyze_food_image():
    """
    Analyze food image and return nutrition info
    Accepts: multipart/form-data with 'image' file
    Returns: JSON with food type, portion size, and nutrition
    """
    try:
        # Check if image is in request
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400
        
        file = request.files['image']
        
        # Check if file is empty
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Check file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_ext not in allowed_extensions:
            return jsonify({
                'success': False,
                'error': f'Invalid file type. Allowed: {", ".join(allowed_extensions)}'
            }), 400
        
        # Read image data
        image_data = file.read()
        
        # Import food recognition module
        try:
            from food_recognition import analyze_food_image as analyze_image
            
            # Analyze the image
            result = analyze_image(image_data)
            
            return jsonify(result)
            
        except ImportError as e:
            return jsonify({
                'success': False,
                'error': 'Food recognition module not available. Install required dependencies.',
                'details': str(e)
            }), 500
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Failed to analyze image',
                'details': str(e)
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Server error',
            'details': str(e)
        }), 500

@app.route('/api/batch-analyze-food', methods=['POST'])
def batch_analyze_food():
    """
    Analyze multiple food images at once
    Useful for analyzing full meal with multiple items
    """
    try:
        if 'images' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No images provided'
            }), 400
        
        files = request.files.getlist('images')
        
        if len(files) == 0:
            return jsonify({
                'success': False,
                'error': 'No files selected'
            }), 400
        
        # Limit to 5 images per batch
        if len(files) > 5:
            return jsonify({
                'success': False,
                'error': 'Maximum 5 images per batch'
            }), 400
        
        # Import food recognition module
        try:
            from food_recognition import analyze_food_image as analyze_image
            
            results = []
            total_nutrition = {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0,
                'fiber': 0,
                'iron': 0,
                'calcium': 0
            }
            
            for file in files:
                image_data = file.read()
                result = analyze_image(image_data)
                
                if result['success']:
                    results.append(result)
                    # Add to total nutrition
                    for key in total_nutrition:
                        total_nutrition[key] += result['nutrition'][key]
            
            # Round total nutrition
            for key in total_nutrition:
                total_nutrition[key] = round(total_nutrition[key], 2)
            
            return jsonify({
                'success': True,
                'items': results,
                'total_items': len(results),
                'total_nutrition': total_nutrition,
                'timestamp': datetime.now().isoformat()
            })
            
        except ImportError as e:
            return jsonify({
                'success': False,
                'error': 'Food recognition module not available',
                'details': str(e)
            }), 500
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Failed to process images',
                'details': str(e)
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Server error',
            'details': str(e)
        }), 500

@app.route('/api/food-database')
def get_food_database():
    """Get list of supported foods in the recognition database"""
    try:
        from food_recognition import INDIAN_FOOD_DATABASE
        
        foods = []
        for key, data in INDIAN_FOOD_DATABASE.items():
            foods.append({
                'id': key,
                'name': key.replace('_', ' ').title(),
                'category': data['category'],
                'nutrition_per_100g': data['nutrition_per_100g']
            })
        
        return jsonify({
            'success': True,
            'foods': foods,
            'total': len(foods)
        })
    except ImportError:
        return jsonify({
            'success': False,
            'error': 'Food database not available'
        }), 500


# ========================================
# ML RECOMMENDATION SYSTEM ENDPOINTS
# ========================================

@app.route('/ml-recommendations')
def ml_recommendations_page():
    """ML Recommendations page"""
    return render_template('ml_recommendations.html')

@app.route('/api/ml/train', methods=['POST'])
def train_ml_models():
    """Train ML recommendation models"""
    try:
        from ml_recommender import MealRecommendationSystem
        
        recommender = MealRecommendationSystem()
        result = recommender.train_models()
        
        return jsonify({
            'success': True,
            'message': 'ML models trained successfully',
            'details': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ml/recommendations/<int:child_id>', methods=['GET'])
def get_ml_recommendations(child_id):
    """Get ML-powered recommendations for a child"""
    try:
        from ml_recommender import MealRecommendationSystem
        
        recommender = MealRecommendationSystem()
        rec_type = request.args.get('type', 'hybrid')
        top_n = int(request.args.get('top_n', 10))
        
        recommendations = recommender.get_recommendations(
            child_id=child_id,
            recommendation_type=rec_type,
            top_n=top_n
        )
        
        return jsonify({
            'success': True,
            'child_id': child_id,
            'type': rec_type,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ml/similar-children/<int:child_id>', methods=['GET'])
def get_similar_children(child_id):
    """Get similar children for collaborative filtering"""
    try:
        from ml_recommender import MealRecommendationSystem
        
        recommender = MealRecommendationSystem()
        top_n = int(request.args.get('top_n', 5))
        
        similar = recommender.find_similar_children(child_id, top_n=top_n)
        
        return jsonify({
            'success': True,
            'child_id': child_id,
            'similar_children': similar
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ml/weekly-variety', methods=['POST'])
def generate_weekly_variety():
    """Generate 7-day variety plan using ML"""
    try:
        from ml_recommender import MealRecommendationSystem
        
        data = request.json
        child_id = data.get('child_id')
        budget = data.get('budget', 2000)
        
        recommender = MealRecommendationSystem()
        weekly_plan = recommender.generate_weekly_variety(
            child_id=child_id,
            budget=budget
        )
        
        return jsonify({
            'success': True,
            'weekly_plan': weekly_plan
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ml/acceptance-prediction', methods=['POST'])
def predict_meal_acceptance():
    """Predict meal acceptance rate using ML"""
    try:
        from ml_recommender import MealRecommendationSystem
        
        data = request.json
        child_id = data.get('child_id')
        ingredients = data.get('ingredients', [])
        
        recommender = MealRecommendationSystem()
        prediction = recommender.predict_meal_acceptance(
            child_id=child_id,
            ingredients=ingredients
        )
        
        return jsonify({
            'success': True,
            'prediction': prediction
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ml/child-profile/<int:child_id>', methods=['GET'])
def get_ml_child_profile(child_id):
    """Get ML-generated child profile"""
    try:
        from ml_recommender import MealRecommendationSystem
        
        recommender = MealRecommendationSystem()
        profile = recommender.prepare_child_profile(child_id)
        
        if not profile:
            return jsonify({
                'success': False,
                'error': 'Child not found'
            }), 404
        
        return jsonify({
            'success': True,
            'profile': profile
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== MALNUTRITION PREDICTION ROUTES ====================

@app.route('/malnutrition-prediction')
def malnutrition_prediction_page():
    """Malnutrition Risk Prediction page"""
    return render_template('malnutrition_prediction.html')

@app.route('/api/predict-malnutrition/<int:child_id>', methods=['POST'])
def predict_malnutrition(child_id):
    """Predict malnutrition risk for a child"""
    try:
        from malnutrition_predictor import get_predictor
        
        # Get child data
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT id, name, date_of_birth, gender, village
            FROM children WHERE id = %s
        """, (child_id,))
        child = cursor.fetchone()
        
        if not child:
            return jsonify({'success': False, 'error': 'Child not found'}), 404
        
        # Get latest growth data
        cursor.execute("""
            SELECT weight_kg, height_cm, measurement_date as measured_date
            FROM growth_tracking
            WHERE child_id = %s
            ORDER BY measurement_date DESC
            LIMIT 1
        """, (child_id,))
        latest_growth = cursor.fetchone()
        
        if not latest_growth:
            return jsonify({'success': False, 'error': 'No growth data available'}), 404
        
        # Get growth history (last 6 months)
        cursor.execute("""
            SELECT weight_kg as weight, height_cm as height, measurement_date as measured_date,
                   TIMESTAMPDIFF(MONTH, %s, measurement_date) as age_months
            FROM growth_tracking
            WHERE child_id = %s
            AND measurement_date >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
            ORDER BY measurement_date ASC
        """, (child['date_of_birth'], child_id))
        growth_history = cursor.fetchall()
        
        # Calculate age in months
        dob = child['date_of_birth']
        # Convert date to datetime if needed
        if hasattr(dob, 'date'):
            dob_date = dob
        else:
            dob_date = dob
            
        # Ensure both are dates for subtraction
        today = datetime.now().date()
        if isinstance(dob, datetime):
            dob_date = dob.date()
        else:
            dob_date = dob
            
        age_months = ((today - dob_date).days / 30.44)
        
        # Get additional data from request
        request_data = request.json or {}
        
        # Prepare child data
        child_data = {
            'age_months': int(age_months),
            'weight_kg': float(latest_growth['weight_kg']),
            'height_cm': float(latest_growth['height_cm']),
            'gender': child['gender'],
            'meals_per_day': request_data.get('meals_per_day', 3),
            'milk_intake_ml': request_data.get('milk_intake_ml', 500),
            'protein_servings': request_data.get('protein_servings', 2),
            'vegetable_servings': request_data.get('vegetable_servings', 2),
            'illness_days_last_month': request_data.get('illness_days_last_month', 0),
            'diarrhea_recent': request_data.get('diarrhea_recent', False),
            'fever_recent': request_data.get('fever_recent', False)
        }
        
        # Get predictor and make prediction
        predictor = get_predictor()
        result = predictor.predict_risk(child_data, growth_history)
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'child': {
                'id': child['id'],
                'name': child['name'],
                'age_months': int(age_months),
                'gender': child['gender']
            },
            'prediction': result
        })
        
    except Exception as e:
        print(f"Error predicting malnutrition: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/malnutrition-stats', methods=['GET'])
def get_malnutrition_stats():
    """Get malnutrition statistics for all children"""
    try:
        from malnutrition_predictor import get_predictor
        
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get all children with growth data
        cursor.execute("""
            SELECT c.id, c.name, c.date_of_birth, c.gender,
                   g.weight_kg, g.height_cm
            FROM children c
            JOIN growth_tracking g ON c.id = g.child_id
            WHERE g.id = (
                SELECT MAX(id) FROM growth_tracking WHERE child_id = c.id
            )
        """)
        children = cursor.fetchall()
        
        predictor = get_predictor()
        stats = {
            'total_children': len(children),
            'high_risk': 0,
            'medium_risk': 0,
            'low_risk': 0,
            'underweight_cases': 0,
            'stunting_cases': 0,
            'wasting_cases': 0,
            'children_at_risk': []
        }
        
        for child in children:
            age_months = int(((datetime.now() - child['date_of_birth']).days / 30.44))
            
            child_data = {
                'age_months': age_months,
                'weight_kg': float(child['weight_kg']),
                'height_cm': float(child['height_cm']),
                'gender': child['gender'],
                'meals_per_day': 3,
                'milk_intake_ml': 500,
                'protein_servings': 2,
                'vegetable_servings': 2,
                'illness_days_last_month': 0,
                'diarrhea_recent': False,
                'fever_recent': False
            }
            
            result = predictor.predict_risk(child_data)
            risk_level = result['overall_risk']
            
            if risk_level == 'high' or risk_level == 'critical':
                stats['high_risk'] += 1
                stats['children_at_risk'].append({
                    'id': child['id'],
                    'name': child['name'],
                    'risk_level': risk_level,
                    'predictions': result['predictions']
                })
            elif risk_level == 'medium':
                stats['medium_risk'] += 1
            else:
                stats['low_risk'] += 1
            
            # Count specific conditions
            if result['predictions'].get('underweight', {}).get('current_status'):
                stats['underweight_cases'] += 1
            if result['predictions'].get('stunting', {}).get('current_status'):
                stats['stunting_cases'] += 1
            if result['predictions'].get('wasting', {}).get('current_status'):
                stats['wasting_cases'] += 1
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        print(f"Error getting malnutrition stats: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print("="*60)
    print("AI NUTRITION ADVISOR - FULL VERSION")
    print("="*60)
    print(f"Starting server on http://0.0.0.0:{port}")
    print("All 60+ features enabled")
    print("="*60)
    
    try:
        # Use waitress for production-ready WSGI server
        from waitress import serve
        serve(app, host='0.0.0.0', port=port, threads=4)
    except ImportError:
        # Fallback to Flask development server
        print("Waitress not available, using Flask dev server")
        app.run(debug=False, host='0.0.0.0', port=port, threaded=True)

