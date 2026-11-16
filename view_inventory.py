
import sqlite3

# Connect to the database
connection = sqlite3.connect("inventory.db")

cursor = connection.cursor()

# Retrieve all inventory records
cursor.execute("SELECT * FROM inventory")

# Fetch all records
records = cursor.fetchall()

# Display records
print("\nINVENTORY RECORDS")
print("-------------------------")

for record in records:
    print(record)

# Close database connection
connection.close()
