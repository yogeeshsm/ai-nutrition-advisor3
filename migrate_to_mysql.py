"""
SQLite to MySQL Migration Tool
Migrates data from SQLite database to MySQL
"""

import sqlite3
import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime
from db_config import SQLITE_DB_PATH, MYSQL_CONFIG
from mysql_schema import get_create_table_statements

def create_mysql_database():
    """Create MySQL database if it doesn't exist"""
    try:
        # Connect without specifying database
        config = MYSQL_CONFIG.copy()
        db_name = config.pop('database')
        
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✓ Database '{db_name}' created/verified")
        
        cursor.close()
        conn.close()
        return True
        
    except Error as e:
        print(f"✗ Error creating database: {e}")
        return False

def create_mysql_tables():
    """Create all tables in MySQL database"""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        statements = get_create_table_statements()
        
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)
                # Extract table name for logging
                table_name = statement.split('TABLE IF NOT EXISTS')[1].split('(')[0].strip()
                print(f"✓ Created table: {table_name}")
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
        
    except Error as e:
        print(f"✗ Error creating tables: {e}")
        return False

def get_sqlite_tables():
    """Get list of tables from SQLite database"""
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

def migrate_table_data(table_name):
    """Migrate data from SQLite table to MySQL table"""
    try:
        # Connect to SQLite
        sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
        sqlite_conn.row_factory = sqlite3.Row
        sqlite_cursor = sqlite_conn.cursor()
        
        # Connect to MySQL
        mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
        mysql_cursor = mysql_conn.cursor()
        
        # Get all rows from SQLite
        sqlite_cursor.execute(f"SELECT * FROM {table_name}")
        rows = sqlite_cursor.fetchall()
        
        if not rows:
            print(f"  ⊘ Table '{table_name}' is empty")
            sqlite_conn.close()
            mysql_conn.close()
            return True
        
        # Get column names
        columns = [description[0] for description in sqlite_cursor.description]
        
        # Filter out 'id' column if it's auto-increment
        columns_without_id = [col for col in columns if col != 'id']
        
        # Prepare INSERT statement
        placeholders = ', '.join(['%s'] * len(columns_without_id))
        columns_str = ', '.join(columns_without_id)
        insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
        
        # Insert data
        inserted = 0
        for row in rows:
            values = [row[col] for col in columns_without_id]
            mysql_cursor.execute(insert_sql, values)
            inserted += 1
        
        mysql_conn.commit()
        print(f"✓ Migrated {inserted} rows to '{table_name}'")
        
        sqlite_conn.close()
        mysql_conn.close()
        return True
        
    except Error as e:
        print(f"✗ Error migrating table '{table_name}': {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error migrating '{table_name}': {e}")
        return False

def verify_migration():
    """Verify that migration was successful by comparing row counts"""
    try:
        sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
        mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
        
        tables = get_sqlite_tables()
        
        print("\n=== Migration Verification ===")
        all_match = True
        
        for table in tables:
            # Get SQLite count
            sqlite_cursor = sqlite_conn.cursor()
            sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table}")
            sqlite_count = sqlite_cursor.fetchone()[0]
            
            # Get MySQL count
            mysql_cursor = mysql_conn.cursor()
            mysql_cursor.execute(f"SELECT COUNT(*) FROM {table}")
            mysql_count = mysql_cursor.fetchone()[0]
            
            if sqlite_count == mysql_count:
                print(f"✓ {table}: {sqlite_count} rows (matched)")
            else:
                print(f"✗ {table}: SQLite={sqlite_count}, MySQL={mysql_count} (mismatch)")
                all_match = False
        
        sqlite_conn.close()
        mysql_conn.close()
        
        return all_match
        
    except Exception as e:
        print(f"✗ Error verifying migration: {e}")
        return False

def run_migration():
    """Run complete migration from SQLite to MySQL"""
    print("=" * 60)
    print("SQLite to MySQL Migration")
    print("=" * 60)
    
    # Step 1: Create MySQL database
    print("\n[Step 1] Creating MySQL database...")
    if not create_mysql_database():
        print("\n✗ Migration failed at database creation")
        return False
    
    # Step 2: Create tables
    print("\n[Step 2] Creating MySQL tables...")
    if not create_mysql_tables():
        print("\n✗ Migration failed at table creation")
        return False
    
    # Step 3: Migrate data
    print("\n[Step 3] Migrating data...")
    tables = get_sqlite_tables()
    
    for table in tables:
        print(f"\nMigrating table: {table}")
        if not migrate_table_data(table):
            print(f"\n⚠ Warning: Failed to migrate table '{table}'")
    
    # Step 4: Verify migration
    print("\n[Step 4] Verifying migration...")
    if verify_migration():
        print("\n" + "=" * 60)
        print("✓ Migration completed successfully!")
        print("=" * 60)
        return True
    else:
        print("\n" + "=" * 60)
        print("⚠ Migration completed with warnings")
        print("=" * 60)
        return True

if __name__ == "__main__":
    print("\n⚠ WARNING: This will migrate data from SQLite to MySQL")
    print(f"Source: {SQLITE_DB_PATH}")
    print(f"Target: {MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}")
    print("\nMake sure:")
    print("1. MySQL server is running")
    print("2. MySQL credentials in db_config.py are correct")
    print("3. You have a backup of your SQLite database")
    
    response = input("\nProceed with migration? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        run_migration()
    else:
        print("\nMigration cancelled")
