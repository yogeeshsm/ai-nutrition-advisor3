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
            serving_size_g REAL DEFAULT 100,
            is_vegetarian INTEGER DEFAULT 1,
            is_vegan INTEGER DEFAULT 0,
            allergens TEXT,
            dietary_tags TEXT
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
    
    # Create children table for immunisation tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS children (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date_of_birth DATE NOT NULL,
            gender TEXT,
            parent_name TEXT,
            phone_number TEXT,
            address TEXT,
            village TEXT,
            health_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create immunisation schedule table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS immunisation_schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_id INTEGER,
            vaccine_name TEXT NOT NULL,
            due_date DATE NOT NULL,
            administered_date DATE,
            status TEXT DEFAULT 'Pending',
            notes TEXT,
            reminder_sent INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (child_id) REFERENCES children(id)
        )
    """)
    
    # Create health information table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_information (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease_name TEXT NOT NULL,
            category TEXT,
            symptoms TEXT,
            prevention TEXT,
            treatment TEXT,
            precautions TEXT,
            age_group TEXT,
            severity TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create growth tracking table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS growth_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_id INTEGER NOT NULL,
            measurement_date DATE NOT NULL,
            weight_kg REAL NOT NULL,
            height_cm REAL NOT NULL,
            bmi REAL,
            head_circumference_cm REAL,
            muac_cm REAL,
            notes TEXT,
            measured_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (child_id) REFERENCES children(id)
        )
    """)
    
    # Create dietary preferences table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dietary_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_id INTEGER NOT NULL,
            is_vegetarian INTEGER DEFAULT 0,
            is_vegan INTEGER DEFAULT 0,
            is_halal INTEGER DEFAULT 0,
            is_kosher INTEGER DEFAULT 0,
            allergies TEXT,
            food_dislikes TEXT,
            medical_restrictions TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (child_id) REFERENCES children(id)
        )
    """)
    
    conn.commit()
    
    # Check if ingredients table is empty
    cursor.execute("SELECT COUNT(*) FROM ingredients")
    if cursor.fetchone()[0] == 0:
        insert_sample_ingredients(conn)
    
    # Check if health_information table is empty
    cursor.execute("SELECT COUNT(*) FROM health_information")
    if cursor.fetchone()[0] == 0:
        insert_health_information(conn)
    
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

def insert_health_information(conn):
    """Insert common child health information"""
    cursor = conn.cursor()
    
    health_data = [
        # Disease name, category, symptoms, prevention, treatment, precautions, age_group, severity
        (
            "Malnutrition", "Nutrition", 
            "Weight loss, fatigue, weakness, slow growth, weak immunity, dry skin",
            "Balanced diet with proteins, vitamins, minerals; Regular health checkups; Breastfeeding for infants",
            "Nutritious diet plan, protein supplements, vitamin supplements, regular monitoring",
            "Ensure 5 meals per day; Include eggs, milk, pulses; Monitor weight monthly; Consult nutritionist",
            "0-10 years", "High"
        ),
        (
            "Diarrhea", "Digestive",
            "Loose watery stools, stomach cramps, fever, dehydration, loss of appetite",
            "Clean drinking water, proper handwashing, food hygiene, avoid contaminated food",
            "ORS (Oral Rehydration Solution), zinc supplements, continue feeding, seek medical help if severe",
            "Give ORS frequently; Continue breastfeeding; Avoid junk food; Maintain hygiene; Watch for dehydration signs",
            "0-10 years", "Medium"
        ),
        (
            "Anemia", "Blood Disorder",
            "Pale skin, fatigue, weakness, dizziness, rapid heartbeat, shortness of breath",
            "Iron-rich diet (leafy vegetables, eggs, meat); Vitamin C foods; Iron supplements",
            "Iron and folic acid supplements, vitamin B12, nutritious diet, regular blood tests",
            "Include spinach, dates, ragi in diet; Take iron tablets with vitamin C; Avoid tea/coffee with meals",
            "1-10 years", "High"
        ),
        (
            "Common Cold", "Respiratory",
            "Runny nose, sneezing, cough, mild fever, sore throat, body ache",
            "Avoid contact with sick people; Hand hygiene; Warm clothing; Boost immunity with nutritious food",
            "Rest, warm liquids, steam inhalation, paracetamol for fever, avoid antibiotics unless prescribed",
            "Keep child warm; Give warm water; Ensure rest; Avoid cold foods; Monitor temperature",
            "0-10 years", "Low"
        ),
        (
            "Measles", "Viral Infection",
            "High fever, red rash, cough, runny nose, red watery eyes, white spots in mouth",
            "Measles vaccination (MMR vaccine); Avoid contact with infected children",
            "Vitamin A supplements, fever management, rest, isolation, medical consultation",
            "Isolate from other children; Give vitamin A; Manage fever; Ensure hydration; Immediate doctor visit",
            "0-6 years", "High"
        ),
        (
            "Chicken Pox", "Viral Infection",
            "Itchy red rashes with blisters, fever, tiredness, loss of appetite, headache",
            "Varicella vaccine; Avoid contact with infected persons",
            "Calamine lotion for itching, paracetamol for fever, antiviral medicines if severe, rest",
            "Keep nails trimmed; Apply calamine; Prevent scratching; Isolate child; Light cotton clothes",
            "1-10 years", "Medium"
        ),
        (
            "Pneumonia", "Respiratory",
            "High fever, cough with phlegm, rapid breathing, chest pain, difficulty breathing",
            "Complete vaccination; Good nutrition; Avoid smoke exposure; Handwashing",
            "Antibiotics, oxygen therapy if needed, hospitalization for severe cases, chest physiotherapy",
            "Immediate medical attention; Keep child warm; Give prescribed medicines; Monitor breathing; Ensure rest",
            "0-5 years", "High"
        ),
        (
            "Tuberculosis (TB)", "Bacterial Infection",
            "Persistent cough, fever, night sweats, weight loss, loss of appetite, fatigue",
            "BCG vaccination at birth; Avoid contact with TB patients; Good ventilation; Nutritious diet",
            "6-9 months anti-TB medicines, directly observed therapy, nutritious diet, regular follow-up",
            "Complete full medicine course; Never skip doses; Ensure good nutrition; Isolate initially; Regular checkups",
            "0-10 years", "High"
        ),
        (
            "Worm Infestation", "Parasitic",
            "Stomach pain, diarrhea, nausea, weight loss, visible worms in stool, itching around anus",
            "Clean drinking water; Handwashing before meals; Wear footwear; Cook food properly; Regular deworming",
            "Deworming tablets (Albendazole/Mebendazole), repeat after 2 weeks, improve hygiene",
            "Deworming every 6 months; Wash hands frequently; Cut nails short; Wear slippers; Boil drinking water",
            "1-10 years", "Medium"
        ),
        (
            "Vitamin A Deficiency", "Nutrition",
            "Night blindness, dry eyes, frequent infections, poor growth, dry skin",
            "Vitamin A rich foods (carrots, papaya, mango, leafy vegetables, eggs, milk)",
            "Vitamin A supplements, nutritious diet, regular eye checkups",
            "Include orange/yellow fruits; Give green leafy vegetables; Vitamin A dose every 6 months; Eye checkups",
            "6 months-5 years", "Medium"
        ),
        (
            "Scabies", "Skin Infection",
            "Intense itching (worse at night), rash, small blisters, burrow tracks on skin",
            "Personal hygiene; Don't share clothes/bedding; Regular bathing; Clean environment",
            "Permethrin cream, oral antihistamines for itching, wash all clothes and bedding in hot water",
            "Apply prescribed cream; Wash all clothes; Bathe daily; Treat all family members; Avoid scratching",
            "0-10 years", "Low"
        ),
        (
            "Dental Cavities", "Dental",
            "Tooth pain, sensitivity to hot/cold, visible holes in teeth, bad breath, discoloration",
            "Brush twice daily; Avoid sugary foods; Regular dental checkups; Fluoride toothpaste",
            "Dental fillings, fluoride treatment, extraction if needed, pain management",
            "Brush morning and night; Limit sweets; Rinse after meals; Visit dentist every 6 months; Use fluoride toothpaste",
            "2-10 years", "Low"
        )
    ]
    
    cursor.executemany("""
        INSERT INTO health_information 
        (disease_name, category, symptoms, prevention, treatment, precautions, age_group, severity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, health_data)
    
    conn.commit()
    print("✅ Health information added successfully!")

# Child and Immunisation Management Functions

def add_child(name, dob, gender, parent_name, phone, address, village, health_notes=""):
    """Add a new child to the system"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO children (name, date_of_birth, gender, parent_name, phone_number, address, village, health_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, dob, gender, parent_name, phone, address, village, health_notes))
    
    child_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return child_id

def get_all_children():
    """Get all children records"""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM children ORDER BY name", conn)
    conn.close()
    return df

def add_immunisation(child_id, vaccine_name, due_date, notes=""):
    """Add immunisation schedule for a child"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO immunisation_schedule (child_id, vaccine_name, due_date, notes)
        VALUES (?, ?, ?, ?)
    """, (child_id, vaccine_name, due_date, notes))
    
    conn.commit()
    conn.close()

def get_pending_immunisations():
    """Get all pending immunisations"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT i.id, c.name, c.parent_name, c.phone_number, c.village,
               i.vaccine_name, i.due_date, i.notes, i.reminder_sent
        FROM immunisation_schedule i
        JOIN children c ON i.child_id = c.id
        WHERE i.status = 'Pending'
        ORDER BY i.due_date
    """, conn)
    conn.close()
    return df

def mark_immunisation_done(immunisation_id, administered_date, notes=""):
    """Mark an immunisation as completed"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE immunisation_schedule 
        SET status = 'Completed', administered_date = ?, notes = ?
        WHERE id = ?
    """, (administered_date, notes, immunisation_id))
    
    conn.commit()
    conn.close()

def get_health_info_by_category(category=None):
    """Get health information, optionally filtered by category"""
    conn = get_connection()
    if category:
        df = pd.read_sql_query(
            "SELECT * FROM health_information WHERE category = ? ORDER BY disease_name", 
            conn, params=(category,)
        )
    else:
        df = pd.read_sql_query("SELECT * FROM health_information ORDER BY disease_name", conn)
    conn.close()
    return df

def search_health_info(search_term):
    """Search health information by disease name or symptoms"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT * FROM health_information 
        WHERE disease_name LIKE ? OR symptoms LIKE ? OR category LIKE ?
        ORDER BY disease_name
    """, conn, params=(f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
    conn.close()
    return df

# Growth Tracking Functions
def add_growth_measurement(child_id, measurement_date, weight_kg, height_cm, 
                          head_circumference_cm=None, muac_cm=None, 
                          notes='', measured_by=''):
    """Add a new growth measurement for a child"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Calculate BMI
    bmi = round(weight_kg / ((height_cm / 100) ** 2), 2) if height_cm > 0 else None
    
    cursor.execute("""
        INSERT INTO growth_tracking 
        (child_id, measurement_date, weight_kg, height_cm, bmi, 
         head_circumference_cm, muac_cm, notes, measured_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (child_id, measurement_date, weight_kg, height_cm, bmi, 
          head_circumference_cm, muac_cm, notes, measured_by))
    
    conn.commit()
    measurement_id = cursor.lastrowid
    conn.close()
    return measurement_id

def get_child_growth_history(child_id):
    """Get all growth measurements for a specific child"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT gt.*, c.name as child_name, c.date_of_birth, c.gender
        FROM growth_tracking gt
        JOIN children c ON gt.child_id = c.id
        WHERE gt.child_id = ?
        ORDER BY gt.measurement_date DESC
    """, conn, params=(child_id,))
    conn.close()
    return df

def get_latest_growth(child_id):
    """Get the most recent growth measurement for a child"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT * FROM growth_tracking
        WHERE child_id = ?
        ORDER BY measurement_date DESC
        LIMIT 1
    """, conn, params=(child_id,))
    conn.close()
    return df.to_dict('records')[0] if len(df) > 0 else None

def calculate_who_z_scores(age_months, weight_kg, height_cm, gender):
    """
    Calculate WHO Z-scores for weight-for-age, height-for-age, and weight-for-height
    This is a simplified version - in production, use WHO growth standards tables
    """
    # Simplified WHO growth standards (approximate values)
    # In production, use actual WHO tables from: https://www.who.int/tools/child-growth-standards
    
    z_scores = {
        'weight_for_age': 0,
        'height_for_age': 0,
        'weight_for_height': 0,
        'status': 'Normal'
    }
    
    # Simplified calculation (replace with actual WHO standards)
    if gender.lower() == 'male':
        expected_weight = 3.3 + (age_months * 0.45)  # Rough approximation
        expected_height = 50 + (age_months * 1.5)
    else:
        expected_weight = 3.2 + (age_months * 0.42)
        expected_height = 49.5 + (age_months * 1.4)
    
    # Calculate z-scores (simplified)
    z_scores['weight_for_age'] = round((weight_kg - expected_weight) / (expected_weight * 0.15), 2)
    z_scores['height_for_age'] = round((height_cm - expected_height) / (expected_height * 0.08), 2)
    
    # Determine nutritional status
    if z_scores['weight_for_age'] < -3:
        z_scores['status'] = 'Severely Underweight'
    elif z_scores['weight_for_age'] < -2:
        z_scores['status'] = 'Underweight'
    elif z_scores['weight_for_age'] > 2:
        z_scores['status'] = 'Overweight'
    else:
        z_scores['status'] = 'Normal'
    
    return z_scores

def get_growth_chart_data(child_id):
    """Get formatted data for growth charts"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT 
            gt.measurement_date,
            gt.weight_kg,
            gt.height_cm,
            gt.bmi,
            gt.head_circumference_cm,
            c.date_of_birth,
            c.gender
        FROM growth_tracking gt
        JOIN children c ON gt.child_id = c.id
        WHERE gt.child_id = ?
        ORDER BY gt.measurement_date ASC
    """, conn, params=(child_id,))
    conn.close()
    
    # Calculate age in months for each measurement
    if len(df) > 0:
        df['measurement_date'] = pd.to_datetime(df['measurement_date'])
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'])
        df['age_months'] = ((df['measurement_date'] - df['date_of_birth']).dt.days / 30.44).astype(int)
    
    return df

if __name__ == "__main__":
    # Initialize database when run directly
    initialize_database()
    print("\n📊 Sample data:")
    print(get_all_ingredients().head())
