"""
Flask-based AI Nutrition Advisor
Modern web application with beautiful UI for generating meal plans
"""

from flask import Flask, render_template, request, jsonify, send_file, session
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

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'nutrition-advisor-secret-key-2025')

# Initialize database on startup
db.initialize_database()

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
            category_items.append({
                'name': ing['name'],
                'cost': ing['cost_per_kg'],
                'calories': ing['calories_per_100g'],
                'emoji': get_food_emoji(category)
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

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
