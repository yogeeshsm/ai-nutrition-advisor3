import sqlite3

conn = sqlite3.connect('nutrition_advisor.db')
cursor = conn.cursor()

cursor.execute('PRAGMA table_info(children)')
columns = cursor.fetchall()
print('Children table columns:')
for col in columns:
    print(f'  {col[1]} ({col[2]})')

conn.close()
