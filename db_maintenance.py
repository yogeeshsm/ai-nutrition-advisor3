"""
Database Maintenance & Optimization Tools
Prevents data mess, ensures data integrity, and optimizes queries
"""

import sqlite3
from datetime import datetime
import database as db

def cleanup_database():
    """Remove duplicate entries and invalid data"""
    conn = db.get_connection()
    cursor = conn.cursor()
    
    print("🧹 Database Maintenance Starting...")
    print("=" * 60)
    
    # 1. Remove duplicate ingredients
    print("\n1️⃣  Checking for duplicate ingredients...")
    cursor.execute("""
        SELECT name, COUNT(*) as count 
        FROM ingredients 
        GROUP BY LOWER(name) 
        HAVING count > 1
    """)
    duplicates = cursor.fetchall()
    
    if duplicates:
        print(f"   Found {len(duplicates)} duplicate ingredient(s)")
        for name, count in duplicates:
            print(f"   - {name}: {count} copies")
            # Keep only the first one, delete others
            cursor.execute("""
                DELETE FROM ingredients 
                WHERE name IN (
                    SELECT name FROM ingredients 
                    WHERE LOWER(name) = LOWER(?)
                    ORDER BY id DESC 
                    LIMIT ? - 1
                )
            """, (name, count))
    else:
        print("   ✅ No duplicate ingredients found")
    
    # 2. Validate nutrition data
    print("\n2️⃣  Validating nutrition data...")
    cursor.execute("""
        SELECT id, name FROM ingredients 
        WHERE calories_per_100g IS NULL 
        OR calories_per_100g < 0 
        OR calories_per_100g > 900
    """)
    invalid = cursor.fetchall()
    
    if invalid:
        print(f"   ⚠️  Found {len(invalid)} ingredient(s) with invalid calories")
        for ing_id, name in invalid:
            print(f"   - {name}: needs review")
    else:
        print("   ✅ All nutrition data valid")
    
    # 3. Check for orphaned records
    print("\n3️⃣  Checking for orphaned records...")
    cursor.execute("""
        SELECT COUNT(*) FROM meal_plan_items 
        WHERE meal_plan_id NOT IN (SELECT id FROM meal_plans)
    """)
    orphaned_items = cursor.fetchone()[0]
    
    if orphaned_items > 0:
        print(f"   ⚠️  Found {orphaned_items} orphaned meal plan items")
        cursor.execute("""
            DELETE FROM meal_plan_items 
            WHERE meal_plan_id NOT IN (SELECT id FROM meal_plans)
        """)
    else:
        print("   ✅ No orphaned records found")
    
    # 4. Optimize database
    print("\n4️⃣  Optimizing database...")
    cursor.execute("VACUUM")
    print("   ✅ Database optimized")
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ Database maintenance complete!")


def create_data_integrity_checks():
    """Add triggers to prevent bad data entry"""
    conn = db.get_connection()
    cursor = conn.cursor()
    
    print("\n🔒 Setting up data integrity checks...")
    
    # Trigger: Prevent negative calories
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS check_valid_calories
        BEFORE INSERT ON ingredients
        FOR EACH ROW
        WHEN NEW.calories_per_100g < 0 OR NEW.calories_per_100g > 900
        BEGIN
            SELECT RAISE(ABORT, 'Invalid calorie value');
        END
    """)
    
    # Trigger: Prevent negative prices
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS check_valid_price
        BEFORE INSERT ON ingredients
        FOR EACH ROW
        WHEN NEW.cost_per_kg < 0
        BEGIN
            SELECT RAISE(ABORT, 'Price cannot be negative');
        END
    """)
    
    # Trigger: Auto-update last_modified timestamp
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS update_meal_plans_timestamp
        AFTER UPDATE ON meal_plans
        FOR EACH ROW
        BEGIN
            UPDATE meal_plans SET created_at = CURRENT_TIMESTAMP 
            WHERE id = NEW.id;
        END
    """)
    
    conn.commit()
    conn.close()
    print("✅ Data integrity checks enabled")


def get_database_stats():
    """Show database statistics"""
    conn = db.get_connection()
    cursor = conn.cursor()
    
    stats = {}
    
    # Count records in each table
    tables = ['ingredients', 'meal_plans', 'meal_plan_items', 'children', 
              'vaccinations', 'growth_tracking', 'mandi_prices', 'health_information']
    
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            stats[table] = cursor.fetchone()[0]
        except sqlite3.OperationalError:
            stats[table] = 0  # Table doesn't exist yet
    
    conn.close()
    
    print("\n📊 DATABASE STATISTICS")
    print("=" * 60)
    for table, count in stats.items():
        print(f"  {table:.<40} {count:>6} records")
    print("=" * 60)
    
    return stats


def create_backup():
    """Create timestamped database backup"""
    import shutil
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"nutrition_advisor_backup_{timestamp}.db"
    
    try:
        shutil.copy("nutrition_advisor.db", backup_path)
        print(f"\n✅ Database backed up to: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return None


if __name__ == "__main__":
    print("\n🛠️  AI NUTRITION ADVISOR - DATABASE MAINTENANCE\n")
    
    # Show current stats
    get_database_stats()
    
    # Create backup before maintenance
    print("\n💾 Creating safety backup...")
    create_backup()
    
    # Run cleanup
    cleanup_database()
    
    # Setup integrity checks
    create_data_integrity_checks()
    
    # Show updated stats
    print("\n📊 Updated statistics:")
    get_database_stats()
    
    print("\n✨ Database is now clean and optimized!")
