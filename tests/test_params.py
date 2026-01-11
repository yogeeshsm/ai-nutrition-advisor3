import sqlite3
import pandas as pd

conn = sqlite3.connect('nutrition_advisor.db')

# Test query with params
child_id = 1
child_query = "SELECT id, name, date_of_birth, gender, village, health_notes FROM children WHERE id = ?"

print(f"Testing query with child_id = {child_id}")
print(f"Query: {child_query}")
print()

# Method 1: Using params
result1 = pd.read_sql_query(child_query, conn, params=(child_id,))
print(f"Method 1 (params tuple): {len(result1)} rows")
if not result1.empty:
    print(result1)
print()

# Method 2: Using params as list
result2 = pd.read_sql_query(child_query, conn, params=[child_id])
print(f"Method 2 (params list): {len(result2)} rows")
if not result2.empty:
    print(result2)
print()

# Method 3: Direct SQL
direct_query = f"SELECT id, name, date_of_birth, gender, village, health_notes FROM children WHERE id = {child_id}"
result3 = pd.read_sql_query(direct_query, conn)
print(f"Method 3 (direct SQL): {len(result3)} rows")
if not result3.empty:
    print(result3)

conn.close()
