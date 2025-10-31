"""
AI Nutrition Advisor for Anganwadi Workers
Streamlit-based demo app for generating balanced weekly meal plans
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import io

# Import custom modules
import database as db
import meal_optimizer as mo
from utils import export_to_pdf, get_food_emoji, translate_text

# Page configuration
st.set_page_config(
    page_title="🍽️ AI Nutrition Advisor",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4ECDC4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stButton>button {
        background-color: #FF6B6B;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #FF5252;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'meal_plan' not in st.session_state:
    st.session_state.meal_plan = None
if 'plan_id' not in st.session_state:
    st.session_state.plan_id = None
if 'language' not in st.session_state:
    st.session_state.language = 'en'

def initialize_app():
    """Initialize database on first run"""
    db.initialize_database()

def main():
    # Initialize
    initialize_app()
    
    # Sidebar
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3655/3655682.png", width=100)
        st.title("⚙️ Settings")
        
        # Language selection (Note: Translation may not be available)
        try:
            from utils import TRANSLATION_AVAILABLE
            if TRANSLATION_AVAILABLE:
                language_option = st.selectbox(
                    "🌐 Language / भाषा",
                    ["English", "Hindi (हिंदी)", "Telugu (తెలుగు)", "Tamil (தமிழ்)"]
                )
                
                language_map = {
                    "English": "en",
                    "Hindi (हिंदी)": "hi",
                    "Telugu (తెలుగు)": "te",
                    "Tamil (தமிழ்)": "ta"
                }
                st.session_state.language = language_map[language_option]
            else:
                st.info("💬 Multi-language feature unavailable (Python 3.13 compatibility)")
                st.session_state.language = 'en'
        except:
            st.session_state.language = 'en'
        
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "📍 Navigate",
            ["🏠 Meal Planner", "📊 Analytics Dashboard", "ℹ️ About"]
        )
        
        st.markdown("---")
        st.info("💡 **Tip**: Select available ingredients and budget to generate optimized meal plans!")
    
    # Main content based on navigation
    if page == "🏠 Meal Planner":
        meal_planner_page()
    elif page == "📊 Analytics Dashboard":
        analytics_page()
    else:
        about_page()

def meal_planner_page():
    """Main meal planner interface"""
    
    # Header
    st.markdown('<div class="main-header">🍽️ AI Nutrition Advisor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Generate Balanced Weekly Meal Plans for Anganwadi Children</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Get ingredients from database
    ingredients_df = db.get_all_ingredients()
    ingredients_by_category = db.get_ingredients_by_category()
    
    # User Input Section
    st.header("📝 Input Details")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        num_children = st.number_input(
            "👶 Number of Children",
            min_value=1,
            max_value=100,
            value=20,
            step=1,
            help="Enter the number of children to plan meals for"
        )
        
        age_group = st.selectbox(
            "👧 Age Group",
            ["1-3 years", "3-6 years", "6-10 years"],
            index=1,
            help="Select the age group for nutritional requirements"
        )
    
    with col2:
        weekly_budget = st.number_input(
            "💰 Weekly Budget (₹)",
            min_value=100.0,
            max_value=50000.0,
            value=2000.0,
            step=100.0,
            help="Total budget for one week's meals"
        )
        
        st.metric("Per Child/Week", f"₹{weekly_budget/num_children:.2f}")
    
    with col3:
        st.metric("Per Child/Day", f"₹{weekly_budget/(num_children*7):.2f}")
        st.metric("Per Meal", f"₹{weekly_budget/(num_children*7*3):.2f}")
    
    st.markdown("---")
    
    # Ingredient Selection
    st.subheader("🥗 Select Available Ingredients")
    
    # Quick selection buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("✅ Select All"):
            st.session_state.selected_ingredients = ingredients_df['name'].tolist()
    with col2:
        if st.button("❌ Clear All"):
            st.session_state.selected_ingredients = []
    with col3:
        if st.button("🌾 Basic Only"):
            st.session_state.selected_ingredients = ingredients_df[
                ingredients_df['category'].isin(['Grains', 'Pulses', 'Vegetables'])
            ]['name'].tolist()
    with col4:
        if st.button("⭐ Recommended"):
            st.session_state.selected_ingredients = [
                'Rice', 'Wheat Flour (Atta)', 'Moong Dal', 'Toor Dal',
                'Potato', 'Onion', 'Tomato', 'Spinach (Palak)',
                'Milk', 'Eggs', 'Cooking Oil', 'Jaggery (Gur)'
            ]
    
    # Multi-select by category
    tabs = st.tabs([f"{get_food_emoji(cat)} {cat}" for cat in ingredients_by_category.keys()])
    
    if 'selected_ingredients' not in st.session_state:
        st.session_state.selected_ingredients = []
    
    selected_ingredients = []
    
    for idx, (category, ingredients_list) in enumerate(ingredients_by_category.items()):
        with tabs[idx]:
            # Show ingredients with emojis and info
            for ingredient in ingredients_list:
                ing_data = ingredients_df[ingredients_df['name'] == ingredient].iloc[0]
                
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    is_selected = st.checkbox(
                        f"{get_food_emoji(category)} {ingredient}",
                        value=ingredient in st.session_state.selected_ingredients,
                        key=f"ing_{ingredient}"
                    )
                    if is_selected:
                        selected_ingredients.append(ingredient)
                with col2:
                    st.caption(f"₹{ing_data['cost_per_kg']}/kg")
                with col3:
                    st.caption(f"🔥 {ing_data['calories_per_100g']:.0f} kcal")
    
    st.session_state.selected_ingredients = selected_ingredients
    
    # Display selection summary
    if selected_ingredients:
        st.success(f"✅ Selected {len(selected_ingredients)} ingredients")
    else:
        st.warning("⚠️ Please select at least a few ingredients to generate meal plan")
    
    st.markdown("---")
    
    # Generate Button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        generate_button = st.button(
            "🚀 Generate Meal Plan",
            use_container_width=True,
            disabled=len(selected_ingredients) == 0
        )
    
    # Generate and Display Meal Plan
    if generate_button:
        with st.spinner("🔄 Optimizing meal plan... Please wait..."):
            try:
                # Create optimizer
                optimizer = mo.MealOptimizer(
                    ingredients_df,
                    weekly_budget,
                    num_children,
                    age_group
                )
                
                # Generate plan
                meal_plan = optimizer.generate_meal_plan(selected_ingredients)
                st.session_state.meal_plan = meal_plan
                
                # Save to database
                plan_data = json.dumps({
                    'weekly_plan': meal_plan['weekly_plan'],
                    'selected_ingredients': selected_ingredients
                }, default=str)
                
                plan_id = db.save_meal_plan(
                    plan_name=f"Plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    budget=weekly_budget,
                    num_children=num_children,
                    age_group=age_group,
                    total_cost=meal_plan['total_cost'],
                    nutrition_score=meal_plan['nutrition_score'],
                    plan_data=plan_data
                )
                st.session_state.plan_id = plan_id
                
                st.success("✅ Meal plan generated successfully!")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Error generating meal plan: {str(e)}")
                st.info("💡 Try adjusting your budget or selecting more ingredients")
    
    # Display results
    if st.session_state.meal_plan:
        display_meal_plan(st.session_state.meal_plan, num_children, weekly_budget)

def display_meal_plan(meal_plan, num_children, budget):
    """Display the generated meal plan"""
    
    st.markdown("---")
    st.header("📋 Your Weekly Meal Plan")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💰 Total Cost",
            f"₹{meal_plan['total_cost']:.2f}",
            f"{((meal_plan['total_cost']/budget - 1) * 100):.1f}% of budget"
        )
    
    with col2:
        score = meal_plan['nutrition_score']
        st.metric(
            "⭐ Nutrition Score",
            f"{score}/100",
            "Excellent" if score >= 85 else "Good" if score >= 70 else "Fair"
        )
    
    with col3:
        daily_calories = meal_plan['weekly_nutrition']['calories'] / 7
        st.metric(
            "🔥 Avg Daily Calories",
            f"{daily_calories:.0f}",
            f"Per child"
        )
    
    with col4:
        daily_protein = meal_plan['weekly_nutrition']['protein'] / 7
        st.metric(
            "💪 Avg Daily Protein",
            f"{daily_protein:.1f}g",
            f"Per child"
        )
    
    st.markdown("---")
    
    # Detailed meal plan table
    st.subheader("🗓️ 7-Day Meal Schedule")
    
    formatted_df = mo.format_meal_plan_for_display(meal_plan)
    
    # Add emoji to ingredients
    formatted_df['Ingredient'] = formatted_df.apply(
        lambda row: f"{get_food_emoji(row['Category'])} {row['Ingredient']}", 
        axis=1
    )
    
    # Style the dataframe
    st.dataframe(
        formatted_df,
        use_container_width=True,
        height=400
    )
    
    # Day-wise tabs
    st.markdown("---")
    st.subheader("📅 Day-wise Breakdown")
    
    days = list(meal_plan['weekly_plan'].keys())
    tabs = st.tabs(days)
    
    for idx, day in enumerate(days):
        with tabs[idx]:
            display_daily_plan(day, meal_plan['weekly_plan'][day])
    
    # Nutritional Analysis
    st.markdown("---")
    display_nutrition_analysis(meal_plan)
    
    # Export options
    st.markdown("---")
    st.subheader("📥 Export Meal Plan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # CSV Export
        csv_buffer = io.StringIO()
        formatted_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📄 Download CSV",
            data=csv_buffer.getvalue(),
            file_name=f"meal_plan_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # JSON Export
        json_data = json.dumps(meal_plan, indent=2, default=str)
        st.download_button(
            label="📋 Download JSON",
            data=json_data,
            file_name=f"meal_plan_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    with col3:
        # PDF Export button
        if st.button("📑 Generate PDF"):
            with st.spinner("Generating PDF..."):
                try:
                    pdf_file = export_to_pdf(meal_plan, num_children, budget)
                    st.download_button(
                        label="💾 Download PDF",
                        data=pdf_file,
                        file_name=f"meal_plan_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")

def display_daily_plan(day, day_plan):
    """Display a single day's meal plan"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        for meal_type, meal_data in day_plan['meals'].items():
            st.markdown(f"### {meal_type.capitalize()} 🍽️")
            
            if meal_data['items']:
                items_text = ", ".join([
                    f"{item['ingredient']} ({item['quantity_per_child_g']:.0f}g)"
                    for item in meal_data['items']
                ])
                st.write(items_text)
                
                # Nutrition info
                st.caption(
                    f"⚡ {meal_data['nutrition']['calories']:.0f} kcal | "
                    f"💪 {meal_data['nutrition']['protein']:.1f}g protein | "
                    f"💰 ₹{meal_data['cost']:.2f}"
                )
            else:
                st.write("No items")
            
            st.markdown("---")
    
    with col2:
        st.markdown("### Daily Summary")
        st.metric("Total Cost", f"₹{day_plan['total_cost']:.2f}")
        st.metric("Calories", f"{day_plan['total_nutrition']['calories']:.0f}")
        st.metric("Protein", f"{day_plan['total_nutrition']['protein']:.1f}g")
        st.metric("Carbs", f"{day_plan['total_nutrition']['carbs']:.1f}g")
        st.metric("Fat", f"{day_plan['total_nutrition']['fat']:.1f}g")

def display_nutrition_analysis(meal_plan):
    """Display nutrition analysis with charts"""
    
    st.subheader("📊 Nutritional Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Macronutrients pie chart
        macro_data = {
            'Protein': meal_plan['weekly_nutrition']['protein'] * 4,  # 4 cal/g
            'Carbs': meal_plan['weekly_nutrition']['carbs'] * 4,
            'Fat': meal_plan['weekly_nutrition']['fat'] * 9  # 9 cal/g
        }
        
        fig_macro = go.Figure(data=[go.Pie(
            labels=list(macro_data.keys()),
            values=list(macro_data.values()),
            hole=.3,
            marker_colors=['#FF6B6B', '#4ECDC4', '#FFE66D']
        )])
        fig_macro.update_layout(
            title="Macronutrient Distribution (Calories)",
            height=350
        )
        st.plotly_chart(fig_macro, use_container_width=True)
    
    with col2:
        # Daily requirements comparison
        weekly_req = {k: v * 7 for k, v in meal_plan['daily_requirements'].items()}
        weekly_actual = meal_plan['weekly_nutrition']
        
        nutrients = ['calories', 'protein', 'carbs', 'fat', 'fiber', 'iron', 'calcium']
        
        comparison_data = []
        for nutrient in nutrients:
            if nutrient in weekly_req and nutrient in weekly_actual:
                comparison_data.append({
                    'Nutrient': nutrient.capitalize(),
                    'Required': weekly_req[nutrient],
                    'Achieved': weekly_actual[nutrient],
                    'Percentage': (weekly_actual[nutrient] / weekly_req[nutrient] * 100) if weekly_req[nutrient] > 0 else 0
                })
        
        df_comparison = pd.DataFrame(comparison_data)
        
        fig_comparison = go.Figure()
        fig_comparison.add_trace(go.Bar(
            name='Required',
            x=df_comparison['Nutrient'],
            y=df_comparison['Required'],
            marker_color='lightblue'
        ))
        fig_comparison.add_trace(go.Bar(
            name='Achieved',
            x=df_comparison['Nutrient'],
            y=df_comparison['Achieved'],
            marker_color='lightgreen'
        ))
        
        fig_comparison.update_layout(
            title="Weekly Nutritional Requirements vs Achieved",
            barmode='group',
            height=350,
            xaxis_title="Nutrients",
            yaxis_title="Amount"
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Percentage achievement
    st.markdown("### 🎯 Target Achievement")
    cols = st.columns(len(comparison_data))
    for idx, row in enumerate(comparison_data):
        with cols[idx]:
            percentage = row['Percentage']
            color = "normal" if 90 <= percentage <= 110 else "off"
            st.metric(
                row['Nutrient'],
                f"{percentage:.0f}%",
                delta=f"{percentage - 100:.0f}%" if percentage != 100 else None,
                delta_color=color
            )

def analytics_page():
    """Admin analytics dashboard"""
    
    st.header("📊 Analytics Dashboard")
    st.markdown("Track meal plan effectiveness and usage patterns")
    
    st.markdown("---")
    
    # Get analytics data
    plans_df, effectiveness_df = db.get_analytics_data()
    
    if len(plans_df) == 0:
        st.info("📭 No meal plans generated yet. Start by creating some meal plans!")
        return
    
    # Summary metrics
    recent_plans = db.get_recent_meal_plans(50)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Total Plans", len(recent_plans))
    
    with col2:
        avg_score = recent_plans['nutrition_score'].mean()
        st.metric("⭐ Avg Nutrition Score", f"{avg_score:.1f}/100")
    
    with col3:
        avg_cost = recent_plans['total_cost'].mean()
        st.metric("💰 Avg Cost", f"₹{avg_cost:.2f}")
    
    with col4:
        avg_children = recent_plans['num_children'].mean()
        st.metric("👶 Avg Children", f"{avg_children:.0f}")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Budget vs Nutrition Score
        if len(effectiveness_df) > 0:
            fig1 = px.scatter(
                effectiveness_df,
                x='budget',
                y='avg_nutrition_score',
                size='avg_cost',
                title="Budget vs Nutrition Score Effectiveness",
                labels={
                    'budget': 'Weekly Budget (₹)',
                    'avg_nutrition_score': 'Avg Nutrition Score'
                }
            )
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Top meal combinations
        if len(plans_df) > 0:
            fig2 = px.bar(
                plans_df.head(10),
                x='count',
                y='age_group',
                orientation='h',
                color='avg_score',
                title="Most Popular Age Group Plans",
                labels={
                    'count': 'Number of Plans',
                    'age_group': 'Age Group',
                    'avg_score': 'Avg Score'
                }
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    # Recent plans table
    st.markdown("---")
    st.subheader("📋 Recent Meal Plans")
    
    display_df = recent_plans[[
        'plan_name', 'budget', 'num_children', 'age_group',
        'total_cost', 'nutrition_score', 'created_at'
    ]].copy()
    
    display_df['created_at'] = pd.to_datetime(display_df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
    
    st.dataframe(display_df, use_container_width=True)

def about_page():
    """About page with information"""
    
    st.header("ℹ️ About AI Nutrition Advisor")
    
    st.markdown("""
    ### 🎯 Purpose
    
    The **AI Nutrition Advisor** is designed to help Anganwadi workers generate balanced, 
    cost-effective weekly meal plans for children using AI-based optimization.
    
    ### ✨ Key Features
    
    - 🤖 **AI-Powered Optimization**: Uses linear programming to maximize nutrition within budget
    - 🍽️ **7-Day Meal Plans**: Complete breakfast, lunch, snack, and dinner for the week
    - 📊 **Nutrition Analysis**: Detailed breakdown of macronutrients and micronutrients
    - 💰 **Budget Management**: Stay within budget while meeting nutritional requirements
    - 📥 **Export Options**: Download plans as CSV, JSON, or PDF
    - 🌐 **Multi-Language Support**: Available in English, Hindi, Telugu, and Tamil
    - 📈 **Analytics Dashboard**: Track effectiveness across different budgets and age groups
    
    ### 🔬 Technology Stack
    
    - **Frontend & Backend**: Streamlit
    - **Database**: SQLite
    - **Optimization**: PuLP (Linear Programming)
    - **Visualization**: Plotly
    - **Data Processing**: Pandas, NumPy
    
    ### 📖 How to Use
    
    1. **Select Ingredients**: Choose from available ingredients in your pantry
    2. **Set Parameters**: Enter budget, number of children, and age group
    3. **Generate Plan**: Click "Generate Meal Plan" button
    4. **Review & Export**: View nutritional analysis and export if needed
    
    ### 🥗 Nutritional Guidelines
    
    The app follows **ICMR (Indian Council of Medical Research)** nutritional guidelines 
    for different age groups of children.
    
    ### 👥 Target Users
    
    - Anganwadi Workers
    - Nutritionists
    - Child Care Centers
    - School Meal Programs
    - NGOs working in nutrition
    
    ### 📞 Support
    
    For questions or feedback, please contact your local Anganwadi coordinator.
    
    ---
    
    **Version**: 1.0.0  
    **Last Updated**: October 2025
    """)
    
    st.success("💚 Made with love for India's children")

if __name__ == "__main__":
    main()
