import sqlite3

connection = sqlite3.connect("budget_manager.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

users = [
    ("Shea", "Mullin", "shea@example.com", "password123"),
    ("Taelynn", "Mullin", "taelynn@example.com", "password123"),
    ("Michael", "Mullin", "michael@example.com", "password123"),
    ("Alex", "Johnson", "alex@example.com", "password123"),
    ("Jordan", "Smith", "jordan@example.com", "password123")
]

cursor.executemany("""
INSERT OR IGNORE INTO users
(first_name, last_name, email, password)
VALUES (?, ?, ?, ?)
""", users)

connection.commit()
connection.close()

print("Database created successfully!")