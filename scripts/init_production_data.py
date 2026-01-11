"""
Production Data Initializer
Ensures sample children data exists on startup (for Render deployment)
"""

import database as db
from datetime import datetime, timedelta
import random

def init_sample_children():
    """Initialize sample children data if database is empty"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Check if children table has any data
        if db.DB_TYPE == 'mysql':
            cursor.execute("SELECT COUNT(*) FROM children")
        else:
            cursor.execute("SELECT COUNT(*) FROM children")
        
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"[OK] Database has {count} children already")
            cursor.close()
            conn.close()
            return
        
        print("[INFO] Initializing sample children data for production...")
        
        # Sample children data (Indian names)
        children_data = [
            ("Lakshmi Iyer", "2019-03-15", "Female", "Priya Iyer", "9876543210", "Anganwadi Center", "Bangalore"),
            ("Arjun Kumar", "2020-06-20", "Male", "Sunita Kumar", "9876543211", "Anganwadi Center", "Bangalore"),
            ("Priya Sharma", "2018-11-10", "Female", "Meera Sharma", "9876543212", "Anganwadi Center", "Bangalore"),
            ("Ravi Patel", "2019-08-05", "Male", "Anjali Patel", "9876543213", "Anganwadi Center", "Bangalore"),
            ("Aisha Khan", "2020-02-28", "Female", "Fatima Khan", "9876543214", "Anganwadi Center", "Bangalore"),
            ("Rohan Singh", "2019-05-17", "Male", "Kavita Singh", "9876543215", "Anganwadi Center", "Bangalore"),
            ("Sneha Reddy", "2020-09-12", "Female", "Lakshmi Reddy", "9876543216", "Anganwadi Center", "Bangalore"),
            ("Karthik Rao", "2018-12-25", "Male", "Suma Rao", "9876543217", "Anganwadi Center", "Bangalore"),
            ("Divya Nair", "2019-07-08", "Female", "Maya Nair", "9876543218", "Anganwadi Center", "Bangalore"),
            ("Amit Gupta", "2020-04-22", "Male", "Rekha Gupta", "9876543219", "Anganwadi Center", "Bangalore"),
            ("Ananya Das", "2019-01-30", "Female", "Jyoti Das", "9876543220", "Anganwadi Center", "Bangalore"),
            ("Vikram Joshi", "2020-08-14", "Male", "Neha Joshi", "9876543221", "Anganwadi Center", "Bangalore"),
            ("Meera Desai", "2018-10-03", "Female", "Pooja Desai", "9876543222", "Anganwadi Center", "Bangalore"),
            ("Siddharth Mehta", "2019-12-19", "Male", "Ritu Mehta", "9876543223", "Anganwadi Center", "Bangalore"),
            ("Ishita Verma", "2020-05-07", "Female", "Priyanka Verma", "9876543224", "Anganwadi Center", "Bangalore")
        ]
        
        # Insert children
        for child_data in children_data:
            if db.DB_TYPE == 'mysql':
                cursor.execute("""
                    INSERT INTO children (name, date_of_birth, gender, parent_name, phone_number, address, village)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, child_data)
            else:
                cursor.execute("""
                    INSERT INTO children (name, date_of_birth, gender, parent_name, phone_number, address, village)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, child_data)
        
        conn.commit()
        
        # Get inserted child IDs
        cursor.execute("SELECT id, date_of_birth FROM children ORDER BY id")
        children = cursor.fetchall()
        
        # Add growth tracking data for each child
        for child in children:
            child_id = child[0]
            dob_str = child[1]
            
            # Parse date
            if isinstance(dob_str, str):
                dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            else:
                dob = dob_str
            
            # Calculate age in months
            today = datetime.now().date()
            age_months = ((today.year - dob.year) * 12 + today.month - dob.month)
            
            # Generate realistic weight and height based on age
            # WHO growth standards (approximate)
            if age_months <= 12:
                weight = 9 + (age_months * 0.4) + random.uniform(-0.5, 0.5)
                height = 75 + (age_months * 1.2) + random.uniform(-2, 2)
            elif age_months <= 24:
                weight = 12 + ((age_months - 12) * 0.3) + random.uniform(-0.5, 0.5)
                height = 85 + ((age_months - 12) * 0.8) + random.uniform(-2, 2)
            elif age_months <= 36:
                weight = 14 + ((age_months - 24) * 0.25) + random.uniform(-0.5, 0.5)
                height = 92 + ((age_months - 24) * 0.6) + random.uniform(-2, 2)
            else:
                weight = 16 + ((age_months - 36) * 0.2) + random.uniform(-0.5, 0.5)
                height = 98 + ((age_months - 36) * 0.5) + random.uniform(-2, 2)
            
            # Add some variation for different nutrition levels
            variation = random.choice([-1, 0, 0, 0, 1])  # Most normal, some under/over
            weight += variation * 1.5
            
            # Add 3 measurement records (last 3 months)
            for i in range(3):
                measurement_date = today - timedelta(days=30 * (2 - i))
                measurement_weight = weight - (2 - i) * 0.3
                measurement_height = height - (2 - i) * 0.8
                
                if db.DB_TYPE == 'mysql':
                    cursor.execute("""
                        INSERT INTO growth_tracking 
                        (child_id, measurement_date, weight_kg, height_cm, muac_cm, measured_by)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (child_id, measurement_date, 
                          round(measurement_weight, 1), 
                          round(measurement_height, 1),
                          round(13.0 + random.uniform(-1, 1), 1),
                          "Health Worker"))
                else:
                    cursor.execute("""
                        INSERT INTO growth_tracking 
                        (child_id, measurement_date, weight_kg, height_cm, muac_cm, measured_by)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (child_id, measurement_date, 
                          round(measurement_weight, 1), 
                          round(measurement_height, 1),
                          round(13.0 + random.uniform(-1, 1), 1),
                          "Health Worker"))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"[OK] Successfully initialized {len(children_data)} sample children")
        print("[OK] Added growth tracking data for all children")
        
    except Exception as e:
        print(f"[ERROR] Failed to initialize sample data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    init_sample_children()
