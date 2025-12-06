"""
Quick script to show MySQL database contents
"""
import mysql.connector
from db_config import MYSQL_CONFIG

# Connect to MySQL
conn = mysql.connector.connect(**MYSQL_CONFIG)
cursor = conn.cursor()

print("\n" + "="*60)
print("MySQL Database Contents")
print("="*60)
print(f"\nDatabase: {MYSQL_CONFIG['database']}")
print(f"Host: {MYSQL_CONFIG['host']}")

# Show all tables
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

print(f"\n📊 Total Tables: {len(tables)}\n")

# For each table, show row count
for (table_name,) in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    status = "✓" if count > 0 else "○"
    print(f"{status} {table_name:30s} : {count:5d} rows")

print("\n" + "="*60)
print("✓ All data is available in MySQL Workbench!")
print("="*60)

print("\nTo view in MySQL Workbench:")
print("1. Open MySQL Workbench")
print(f"2. Connect to: {MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}")
print(f"3. User: {MYSQL_CONFIG['user']}")
print(f"4. Select database: {MYSQL_CONFIG['database']}")
print("5. Browse tables in left sidebar\n")

cursor.close()
conn.close()
