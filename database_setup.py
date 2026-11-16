
import sqlite3
from pathlib import Path

# Use the same database location as database.py.
BASE_DIR = Path(__file__).parent
DATABASE_PATH = BASE_DIR / "inventory.db"

# Connect to the database.
connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

# 1. Create the inventory table.
cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    available_stock INTEGER NOT NULL,
    minimum_stock INTEGER NOT NULL,
    price REAL NOT NULL
)
""")

# 2. Create the users table.
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'user'))
)
""")

# 3. Create the stock audit table.
cursor.execute("""
CREATE TABLE IF NOT EXISTS stock_audit (
    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    old_quantity INTEGER NOT NULL,
    new_quantity INTEGER NOT NULL,
    approved_by_user_id INTEGER NOT NULL,
    approved_by_username TEXT NOT NULL,
    approved_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
)
""")

# Save all database changes.
connection.commit()

# Close the connection.
connection.close()

print("Inventory database created successfully!")
