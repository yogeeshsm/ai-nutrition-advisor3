-- MySQL Workbench Test Script
-- Copy and paste this entire script into MySQL Workbench

-- Select the database
USE nutrition_advisor;

-- Show all tables
SHOW TABLES;

-- Check ingredients (66 rows)
SELECT COUNT(*) as total_ingredients FROM ingredients;
SELECT * FROM ingredients LIMIT 10;

-- Check children (8 rows)
SELECT COUNT(*) as total_children FROM children;
SELECT * FROM children;

-- Check growth tracking (8 rows)
SELECT COUNT(*) as total_growth_records FROM growth_tracking;
SELECT * FROM growth_tracking;

-- Check health information (12 rows)
SELECT COUNT(*) as total_health_records FROM health_information;
SELECT * FROM health_information;

-- Join children with growth tracking
SELECT 
    c.name,
    c.date_of_birth,
    g.measurement_date,
    g.weight_kg,
    g.height_cm,
    g.bmi
FROM children c
LEFT JOIN growth_tracking g ON c.id = g.child_id
ORDER BY c.name, g.measurement_date;

-- Summary statistics
SELECT 
    'ingredients' as table_name, COUNT(*) as row_count FROM ingredients
UNION ALL
SELECT 'children', COUNT(*) FROM children
UNION ALL
SELECT 'growth_tracking', COUNT(*) FROM growth_tracking
UNION ALL
SELECT 'health_information', COUNT(*) FROM health_information
UNION ALL
SELECT 'child_identity_cards', COUNT(*) FROM child_identity_cards;
