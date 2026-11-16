
import sqlite3
from inventory_data import inventory

# Connect to our database
connection = sqlite3.connect("inventory.db")

cursor = connection.cursor()

# Insert inventory records
for product in inventory:
    cursor.execute("""
        INSERT OR REPLACE INTO inventory
        (product_id, product_name, available_stock, minimum_stock, price)
        VALUES (?, ?, ?, ?, ?)
    """, (
        product["product_id"],
        product["product_name"],
        product["available_stock"],
        product["minimum_stock"],
        product["price"]
    ))

# Save changes
connection.commit()

# Close connection
connection.close()

print("Inventory records inserted successfully!")
