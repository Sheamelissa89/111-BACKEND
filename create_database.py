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



cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    expense_date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

expenses = [
    (1, "Groceries", 120.50, "Food", "2026-08-03"),
    (2, "Gas", 55.25, "Transportation", "2026-08-03"),
    (3, "Electric Bill", 145.00, "Utilities", "2026-08-03"),
    (4, "Internet", 79.99, "Utilities", "2026-08-03"),
    (5, "Coffee", 8.50, "Food", "2026-08-03")
]

cursor.executemany("""
INSERT OR IGNORE INTO expenses
(user_id, description, amount, category, expense_date)
VALUES (?, ?, ?, ?, ?)
""", expenses)

connection.commit()
connection.close()

print("Database created successfully!")