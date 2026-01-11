import sqlite3

conn = sqlite3.connect('nutrition_advisor.db')
cursor = conn.cursor()

# Check if table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='child_identity_cards'")
result = cursor.fetchone()

if result:
    print("✅ Table 'child_identity_cards' EXISTS")
    # Show structure
    cursor.execute("PRAGMA table_info(child_identity_cards)")
    columns = cursor.fetchall()
    print("\nTable structure:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
else:
    print("❌ Table 'child_identity_cards' does NOT exist")
    print("\nCreating table...")
    cursor.execute("""
        CREATE TABLE child_identity_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_id INTEGER NOT NULL,
            card_number TEXT NOT NULL,
            qr_code_id TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (child_id) REFERENCES children (id),
            UNIQUE(child_id)
        )
    """)
    conn.commit()
    print("✅ Table created successfully!")

conn.close()
