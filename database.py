"""
Database module for Nutrition Advisor
Handles SQLite database operations for ingredients and meal plans
"""

import sqlite3
import pandas as pd
from datetime import datetime
import os

DATABASE_PATH = "nutrition_advisor.db"

def get_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    return conn

def initialize_database():
    """Initialize database with tables and sample data"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create ingredients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            cost_per_kg REAL NOT NULL,
            protein_per_100g REAL,
            carbs_per_100g REAL,
            fat_per_100g REAL,
            calories_per_100g REAL,
            fiber_per_100g REAL,
            iron_per_100g REAL,
            calcium_per_100g REAL,
            serving_size_g REAL DEFAULT 100
        )
    """)
    
    # Create meal_plans table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meal_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_name TEXT,
            budget REAL,
            num_children INTEGER,
            age_group TEXT,
            total_cost REAL,
            nutrition_score REAL,
            plan_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create feedback table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meal_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_id INTEGER,
            rating INTEGER,
            comments TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (plan_id) REFERENCES meal_plans(id)
        )
    """)
    
    conn.commit()
    
    # Check if ingredients table is empty
    cursor.execute("SELECT COUNT(*) FROM ingredients")
    if cursor.fetchone()[0] == 0:
        insert_sample_ingredients(conn)
    
    conn.close()
    print("✅ Database initialized successfully!")

def insert_sample_ingredients(conn):
    """Insert sample Indian ingredients with nutritional data"""
    ingredients = [
        # Grains & Cereals (cost per kg in INR)
        ("Rice", "Grains", 45, 7.0, 77.0, 0.5, 360, 1.3, 0.8, 10, 100),
        ("Wheat Flour (Atta)", "Grains", 35, 11.0, 71.0, 1.5, 340, 11.0, 3.5, 30, 100),
        ("Jowar (Sorghum)", "Grains", 50, 10.4, 70.7, 1.9, 329, 9.7, 4.1, 25, 100),
        ("Ragi (Finger Millet)", "Grains", 60, 7.3, 72.0, 1.3, 328, 3.6, 3.9, 344, 100),
        ("Poha (Flattened Rice)", "Grains", 55, 6.6, 76.9, 1.4, 350, 0.3, 20.0, 20, 100),
        
        # Pulses & Legumes
        ("Moong Dal", "Pulses", 120, 24.0, 59.0, 1.2, 347, 16.0, 6.7, 124, 100),
        ("Toor Dal", "Pulses", 100, 22.0, 62.0, 1.5, 335, 15.0, 2.7, 73, 100),
        ("Chana Dal", "Pulses", 90, 20.0, 61.0, 6.0, 360, 13.0, 5.3, 56, 100),
        ("Masoor Dal", "Pulses", 110, 25.0, 60.0, 1.1, 352, 11.0, 7.6, 51, 100),
        ("Rajma (Kidney Beans)", "Pulses", 130, 22.9, 60.0, 1.4, 333, 15.0, 8.2, 143, 100),
        ("Chickpeas (Kabuli Chana)", "Pulses", 80, 19.0, 61.0, 6.0, 364, 17.0, 6.2, 57, 100),
        
        # Vegetables
        ("Potato", "Vegetables", 25, 2.0, 17.0, 0.1, 77, 2.2, 0.8, 12, 150),
        ("Onion", "Vegetables", 30, 1.2, 11.0, 0.1, 40, 1.7, 0.2, 23, 100),
        ("Tomato", "Vegetables", 35, 0.9, 3.9, 0.2, 18, 1.2, 0.5, 10, 150),
        ("Carrot", "Vegetables", 40, 0.9, 10.0, 0.2, 41, 2.8, 0.3, 33, 100),
        ("Spinach (Palak)", "Vegetables", 45, 2.9, 3.6, 0.4, 23, 2.2, 2.7, 99, 100),
        ("Pumpkin", "Vegetables", 20, 1.0, 6.5, 0.1, 26, 0.5, 0.8, 21, 150),
        ("Cabbage", "Vegetables", 25, 1.3, 5.8, 0.1, 25, 2.5, 0.5, 40, 100),
        ("Cauliflower", "Vegetables", 30, 2.0, 5.0, 0.3, 25, 2.0, 0.4, 22, 100),
        ("Green Beans", "Vegetables", 50, 1.8, 7.0, 0.1, 31, 2.7, 1.0, 37, 100),
        ("Brinjal (Eggplant)", "Vegetables", 35, 1.0, 5.9, 0.2, 25, 3.0, 0.3, 9, 150),
        
        # Dairy & Eggs
        ("Milk", "Dairy", 55, 3.2, 4.8, 3.2, 61, 0, 0.0, 113, 250),
        ("Curd (Yogurt)", "Dairy", 60, 3.5, 4.7, 4.0, 60, 0, 0.1, 120, 150),
        ("Eggs", "Protein", 6, 13.0, 1.1, 11.0, 155, 0, 1.8, 50, 50),
        ("Paneer", "Dairy", 300, 18.0, 1.2, 20.0, 265, 0, 0.2, 208, 100),
        
        # Oils & Fats
        ("Cooking Oil", "Fats", 150, 0, 0, 100.0, 884, 0, 0, 0, 10),
        ("Ghee", "Fats", 500, 0, 0, 99.5, 876, 0, 0, 4, 10),
        
        # Dry Fruits & Nuts
        ("Almonds", "Dry Fruits", 700, 21.0, 22.0, 50.0, 579, 12.5, 3.7, 264, 30),
        ("Cashews", "Dry Fruits", 800, 18.0, 30.0, 44.0, 553, 3.3, 6.7, 37, 30),
        ("Raisins (Kishmish)", "Dry Fruits", 400, 3.1, 79.0, 0.5, 299, 3.7, 1.9, 50, 30),
        ("Dates (Khajoor)", "Dry Fruits", 350, 2.5, 75.0, 0.4, 282, 8.0, 1.0, 39, 40),
        ("Walnuts", "Dry Fruits", 900, 15.0, 14.0, 65.0, 654, 6.7, 2.9, 98, 30),
        ("Peanuts", "Dry Fruits", 150, 26.0, 16.0, 49.0, 567, 8.5, 4.6, 92, 30),
        ("Groundnuts", "Dry Fruits", 120, 25.8, 16.1, 49.2, 567, 8.5, 4.6, 92, 30),
        
        # Fresh Fruits
        ("Banana", "Fruits", 40, 1.1, 23.0, 0.3, 89, 2.6, 0.3, 5, 120),
        ("Apple", "Fruits", 120, 0.3, 14.0, 0.2, 52, 2.4, 0.1, 6, 150),
        ("Papaya", "Fruits", 30, 0.5, 11.0, 0.1, 43, 1.7, 0.3, 20, 150),
        ("Mango", "Fruits", 80, 0.8, 15.0, 0.4, 60, 1.6, 0.2, 11, 150),
        ("Orange", "Fruits", 60, 0.9, 12.0, 0.1, 47, 2.4, 0.1, 40, 150),
        ("Guava", "Fruits", 50, 2.6, 14.0, 0.9, 68, 5.4, 0.3, 18, 150),
        ("Pomegranate", "Fruits", 150, 1.7, 19.0, 1.2, 83, 4.0, 0.3, 10, 150),
        ("Watermelon", "Fruits", 25, 0.6, 8.0, 0.2, 30, 0.4, 0.2, 7, 200),
        ("Grapes", "Fruits", 80, 0.7, 18.0, 0.2, 69, 0.9, 0.4, 10, 100),
        ("Pineapple", "Fruits", 50, 0.5, 13.0, 0.1, 50, 1.4, 0.3, 13, 150),
        
        # Leafy Vegetables
        ("Spinach (Palak) Fresh", "Leafy Vegetables", 40, 2.9, 3.6, 0.4, 23, 2.2, 2.7, 99, 100),
        ("Fenugreek Leaves (Methi)", "Leafy Vegetables", 50, 4.4, 6.0, 0.9, 49, 25.0, 33.5, 395, 100),
        ("Mustard Greens (Sarson)", "Leafy Vegetables", 45, 3.0, 4.5, 0.4, 27, 3.2, 2.0, 115, 100),
        ("Amaranth Leaves (Chaulai)", "Leafy Vegetables", 50, 4.6, 4.0, 0.5, 23, 2.6, 5.4, 215, 100),
        ("Curry Leaves", "Leafy Vegetables", 200, 6.1, 18.7, 1.0, 108, 6.4, 0.9, 830, 20),
        ("Coriander Leaves (Dhania)", "Leafy Vegetables", 80, 3.3, 3.7, 0.5, 23, 2.8, 1.8, 67, 50),
        ("Mint Leaves (Pudina)", "Leafy Vegetables", 100, 3.8, 8.4, 0.7, 44, 6.8, 11.9, 199, 50),
        ("Radish Greens", "Leafy Vegetables", 30, 2.0, 3.6, 0.3, 20, 2.5, 1.5, 90, 100),
        ("Drumstick Leaves (Moringa)", "Leafy Vegetables", 60, 9.4, 8.3, 1.4, 64, 2.0, 4.0, 185, 100),
        ("Cabbage (Green)", "Leafy Vegetables", 25, 1.3, 5.8, 0.1, 25, 2.5, 0.5, 40, 100),
        ("Lettuce", "Leafy Vegetables", 150, 1.4, 2.9, 0.2, 15, 1.3, 0.9, 36, 100),
        
        # Nutrition-Rich Foods
        ("Soya Chunks", "Nutrition Rich", 180, 52.0, 33.0, 0.5, 345, 13.0, 20.0, 350, 50),
        ("Oats", "Nutrition Rich", 80, 13.0, 67.0, 7.0, 389, 10.0, 4.7, 54, 100),
        ("Quinoa", "Nutrition Rich", 400, 14.0, 64.0, 6.0, 368, 7.0, 4.6, 47, 100),
        ("Chia Seeds", "Nutrition Rich", 800, 17.0, 42.0, 31.0, 486, 34.4, 7.7, 631, 20),
        ("Flax Seeds (Alsi)", "Nutrition Rich", 200, 18.0, 29.0, 42.0, 534, 27.0, 5.7, 255, 20),
        ("Sunflower Seeds", "Nutrition Rich", 300, 21.0, 20.0, 51.0, 584, 8.6, 5.2, 78, 30),
        ("Pumpkin Seeds", "Nutrition Rich", 500, 30.0, 11.0, 49.0, 559, 6.0, 8.8, 46, 30),
        ("Sesame Seeds (Til)", "Nutrition Rich", 250, 18.0, 23.0, 50.0, 573, 11.8, 14.6, 975, 20),
        
        # Other
        ("Jaggery (Gur)", "Sweetener", 60, 0.4, 98.0, 0.1, 383, 0, 11.0, 80, 20),
        ("Sugar", "Sweetener", 40, 0, 99.9, 0, 387, 0, 0.1, 1, 10),
        ("Honey", "Sweetener", 350, 0.3, 82.0, 0, 304, 0.2, 0.4, 6, 20),
    ]
    
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT OR IGNORE INTO ingredients 
        (name, category, cost_per_kg, protein_per_100g, carbs_per_100g, 
         fat_per_100g, calories_per_100g, fiber_per_100g, iron_per_100g, 
         calcium_per_100g, serving_size_g)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ingredients)
    
    conn.commit()
    print(f"✅ Inserted {len(ingredients)} sample ingredients")

def get_all_ingredients():
    """Retrieve all ingredients as a DataFrame"""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM ingredients", conn)
    conn.close()
    return df

def get_ingredients_by_category():
    """Get ingredients grouped by category"""
    df = get_all_ingredients()
    return df.groupby('category')['name'].apply(list).to_dict()

def save_meal_plan(plan_name, budget, num_children, age_group, total_cost, 
                   nutrition_score, plan_data):
    """Save a generated meal plan to database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO meal_plans 
        (plan_name, budget, num_children, age_group, total_cost, nutrition_score, plan_data)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (plan_name, budget, num_children, age_group, total_cost, nutrition_score, plan_data))
    
    plan_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return plan_id

def get_recent_meal_plans(limit=10):
    """Get recent meal plans"""
    conn = get_connection()
    df = pd.read_sql_query(
        f"SELECT * FROM meal_plans ORDER BY created_at DESC LIMIT {limit}", 
        conn
    )
    conn.close()
    return df

def save_feedback(plan_id, rating, comments):
    """Save user feedback for a meal plan"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO meal_feedback (plan_id, rating, comments)
        VALUES (?, ?, ?)
    """, (plan_id, rating, comments))
    
    conn.commit()
    conn.close()

def get_analytics_data():
    """Get analytics data for admin dashboard"""
    conn = get_connection()
    
    # Top meal combinations
    plans_df = pd.read_sql_query("""
        SELECT budget, num_children, age_group, AVG(nutrition_score) as avg_score,
               AVG(total_cost) as avg_cost, COUNT(*) as count
        FROM meal_plans
        GROUP BY budget, num_children, age_group
        ORDER BY count DESC
        LIMIT 10
    """, conn)
    
    # Budget vs nutrition effectiveness
    effectiveness_df = pd.read_sql_query("""
        SELECT budget, AVG(nutrition_score) as avg_nutrition_score,
               AVG(total_cost) as avg_cost
        FROM meal_plans
        GROUP BY budget
        ORDER BY budget
    """, conn)
    
    conn.close()
    return plans_df, effectiveness_df

if __name__ == "__main__":
    # Initialize database when run directly
    initialize_database()
    print("\n📊 Sample data:")
    print(get_all_ingredients().head())
