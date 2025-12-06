"""
MySQL Database Schema for Nutrition Advisor
Creates all necessary tables in MySQL format
"""

CREATE_TABLES_MYSQL = """
-- Ingredients table
CREATE TABLE IF NOT EXISTS ingredients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    category VARCHAR(100) NOT NULL,
    cost_per_kg DECIMAL(10,2) NOT NULL,
    protein_per_100g DECIMAL(10,2),
    carbs_per_100g DECIMAL(10,2),
    fat_per_100g DECIMAL(10,2),
    calories_per_100g DECIMAL(10,2),
    fiber_per_100g DECIMAL(10,2),
    iron_per_100g DECIMAL(10,2),
    calcium_per_100g DECIMAL(10,2),
    serving_size_g DECIMAL(10,2) DEFAULT 100,
    is_vegetarian TINYINT DEFAULT 1,
    is_vegan TINYINT DEFAULT 0,
    allergens TEXT,
    dietary_tags TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Meal plans table
CREATE TABLE IF NOT EXISTS meal_plans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plan_name VARCHAR(255),
    budget DECIMAL(10,2),
    num_children INT,
    age_group VARCHAR(50),
    total_cost DECIMAL(10,2),
    nutrition_score DECIMAL(10,2),
    plan_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Meal feedback table
CREATE TABLE IF NOT EXISTS meal_feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plan_id INT,
    rating INT,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plan_id) REFERENCES meal_plans(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Children table
CREATE TABLE IF NOT EXISTS children (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(20),
    parent_name VARCHAR(255),
    phone_number VARCHAR(20),
    address TEXT,
    village VARCHAR(255),
    health_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Immunisation schedule table
CREATE TABLE IF NOT EXISTS immunisation_schedule (
    id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT,
    vaccine_name VARCHAR(255) NOT NULL,
    due_date DATE NOT NULL,
    administered_date DATE,
    status VARCHAR(50) DEFAULT 'Pending',
    notes TEXT,
    reminder_sent TINYINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Health information table
CREATE TABLE IF NOT EXISTS health_information (
    id INT AUTO_INCREMENT PRIMARY KEY,
    disease_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    symptoms TEXT,
    prevention TEXT,
    treatment TEXT,
    precautions TEXT,
    age_group VARCHAR(50),
    severity VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Growth tracking table
CREATE TABLE IF NOT EXISTS growth_tracking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT NOT NULL,
    measurement_date DATE NOT NULL,
    weight_kg DECIMAL(10,2) NOT NULL,
    height_cm DECIMAL(10,2) NOT NULL,
    bmi DECIMAL(10,2),
    head_circumference_cm DECIMAL(10,2),
    muac_cm DECIMAL(10,2),
    notes TEXT,
    measured_by VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dietary preferences table
CREATE TABLE IF NOT EXISTS dietary_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT NOT NULL,
    is_vegetarian TINYINT DEFAULT 0,
    is_vegan TINYINT DEFAULT 0,
    is_halal TINYINT DEFAULT 0,
    is_kosher TINYINT DEFAULT 0,
    allergies TEXT,
    food_dislikes TEXT,
    medical_restrictions TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Child identity cards table
CREATE TABLE IF NOT EXISTS child_identity_cards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT NOT NULL UNIQUE,
    qr_code_id VARCHAR(255) NOT NULL UNIQUE,
    qr_code_data TEXT NOT NULL,
    qr_code_image_path VARCHAR(500),
    card_number VARCHAR(100) NOT NULL UNIQUE,
    is_active TINYINT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Emergency contacts table
CREATE TABLE IF NOT EXISTS emergency_contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT NOT NULL,
    contact_name VARCHAR(255) NOT NULL,
    contact_type VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    relationship VARCHAR(100),
    priority INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Family health risks table
CREATE TABLE IF NOT EXISTS family_health_risks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT NOT NULL,
    condition_name VARCHAR(255) NOT NULL,
    severity VARCHAR(50),
    family_member VARCHAR(255),
    description TEXT,
    precautions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Child nutrition snapshot table
CREATE TABLE IF NOT EXISTS child_nutrition_snapshot (
    id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT NOT NULL UNIQUE,
    nutrition_status VARCHAR(100),
    calorie_target INT,
    protein_target DECIMAL(10,2),
    iron_level VARCHAR(50),
    calcium_level VARCHAR(50),
    vitamin_a_level VARCHAR(50),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Vaccination summary table
CREATE TABLE IF NOT EXISTS vaccination_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT NOT NULL UNIQUE,
    total_vaccinations INT,
    completed_vaccinations INT,
    pending_vaccinations INT,
    next_vaccine_name VARCHAR(255),
    next_vaccine_date VARCHAR(50),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

def get_create_table_statements():
    """Split the CREATE_TABLES_MYSQL into individual statements"""
    statements = []
    current_statement = []
    
    for line in CREATE_TABLES_MYSQL.split('\n'):
        line = line.strip()
        if not line or line.startswith('--'):
            continue
        current_statement.append(line)
        if line.endswith(';'):
            statements.append(' '.join(current_statement))
            current_statement = []
    
    return statements
