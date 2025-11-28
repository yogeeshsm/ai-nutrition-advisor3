import sqlite3

conn = sqlite3.connect('nutrition_advisor.db')
cursor = conn.cursor()

cursor.execute('PRAGMA table_info(immunisation_schedule)')
cols = cursor.fetchall()
print('immunisation_schedule columns:')
for col in cols:
    print(f'  {col[1]} ({col[2]})')

conn.close()
