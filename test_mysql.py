"""
MySQL Setup and Test Script
Quick way to verify MySQL is properly configured
"""

import sys
from db_config import MYSQL_CONFIG

def test_mysql_connection():
    """Test MySQL connection with current configuration"""
    print("=" * 60)
    print("MySQL Connection Test")
    print("=" * 60)
    
    try:
        import mysql.connector
        from mysql.connector import Error
        
        print("\n✓ MySQL connector installed")
        
        # Show configuration (hide password)
        config_display = MYSQL_CONFIG.copy()
        config_display['password'] = '*' * len(config_display['password']) if config_display['password'] else '(empty)'
        
        print("\nConfiguration:")
        for key, value in config_display.items():
            if key not in ['charset', 'use_unicode', 'autocommit']:
                print(f"  {key}: {value}")
        
        # Try to connect without database first
        print("\n[Test 1] Connecting to MySQL server...")
        config_no_db = {k: v for k, v in MYSQL_CONFIG.items() if k != 'database'}
        
        try:
            conn = mysql.connector.connect(**config_no_db)
            print("✓ Successfully connected to MySQL server")
            
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            print(f"✓ MySQL version: {version}")
            
            # Check if database exists
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            
            if MYSQL_CONFIG['database'] in databases:
                print(f"✓ Database '{MYSQL_CONFIG['database']}' exists")
            else:
                print(f"⚠ Database '{MYSQL_CONFIG['database']}' does not exist")
                print(f"  Run migrate_to_mysql.py to create it")
            
            cursor.close()
            conn.close()
            
        except Error as e:
            print(f"✗ Connection failed: {e}")
            print("\nTroubleshooting:")
            print("1. Ensure MySQL server is running")
            print("2. Check host and port are correct")
            print("3. Verify username and password in db_config.py")
            return False
        
        # Try to connect with database
        print(f"\n[Test 2] Connecting to database '{MYSQL_CONFIG['database']}'...")
        try:
            conn = mysql.connector.connect(**MYSQL_CONFIG)
            print(f"✓ Successfully connected to '{MYSQL_CONFIG['database']}'")
            
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print(f"✓ Found {len(tables)} tables:")
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                    count = cursor.fetchone()[0]
                    print(f"  - {table[0]}: {count} rows")
            else:
                print("⚠ No tables found in database")
                print("  Run migrate_to_mysql.py to create tables")
            
            cursor.close()
            conn.close()
            
        except Error as e:
            if "Unknown database" in str(e):
                print(f"✗ Database '{MYSQL_CONFIG['database']}' doesn't exist")
                print("\nTo create it, run:")
                print("  python migrate_to_mysql.py")
            else:
                print(f"✗ Error: {e}")
            return False
        
        print("\n" + "=" * 60)
        print("✓ MySQL is properly configured!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Run 'python migrate_to_mysql.py' to migrate data")
        print("2. Set environment: $env:DB_TYPE='mysql'")
        print("3. Start server: python start_server.py")
        
        return True
        
    except ImportError:
        print("✗ MySQL connector not installed")
        print("\nInstall it with:")
        print("  pip install mysql-connector-python")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def show_mysql_commands():
    """Show useful MySQL commands"""
    print("\n" + "=" * 60)
    print("Useful MySQL Commands")
    print("=" * 60)
    
    print("\n# Connect to MySQL:")
    print(f"mysql -u {MYSQL_CONFIG['user']} -p")
    
    print("\n# Create database manually:")
    print(f"CREATE DATABASE {MYSQL_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    
    print("\n# Show databases:")
    print("SHOW DATABASES;")
    
    print("\n# Use database:")
    print(f"USE {MYSQL_CONFIG['database']};")
    
    print("\n# Show tables:")
    print("SHOW TABLES;")
    
    print("\n# Count rows:")
    print("SELECT COUNT(*) FROM children;")
    
    print("\n# Backup database:")
    print(f"mysqldump -u {MYSQL_CONFIG['user']} -p {MYSQL_CONFIG['database']} > backup.sql")
    
    print("\n# Restore database:")
    print(f"mysql -u {MYSQL_CONFIG['user']} -p {MYSQL_CONFIG['database']} < backup.sql")

if __name__ == "__main__":
    success = test_mysql_connection()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        show_mysql_commands()
    
    if not success:
        print("\n⚠ Please fix the issues above before proceeding")
        sys.exit(1)
