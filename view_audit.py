
from database import get_database_connection

connection = get_database_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT
        audit_id,
        product_name,
        old_quantity,
        new_quantity,
        approved_by_username,
        approved_at
    FROM stock_audit
    ORDER BY audit_id
""")

records = cursor.fetchall()

print("\nSTOCK AUDIT HISTORY")
print("-----------------------------")

if records:
    for record in records:
        print(record)
else:
    print("No stock update records found.")

connection.close()
