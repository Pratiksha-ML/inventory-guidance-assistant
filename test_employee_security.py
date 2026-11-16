
from database import get_database_connection
from inventory_update import update_stock_quantity

# Retrieve the employee account from SQLite.
connection = get_database_connection()
cursor = connection.cursor()

cursor.execute(
    """
    SELECT user_id, username, role
    FROM users
    WHERE username = ?
    """,
    ("employee1",)
)

employee = cursor.fetchone()
connection.close()

if employee is None:
    print("Employee account not found.")

else:
    print("\nEMPLOYEE SECURITY TEST")
    print("----------------------")
    print("Username:", employee[1])
    print("Actual database role:", employee[2])

    # Simulate a manipulated role.
    # The database should still reject this employee.
    forged_employee = {
        "user_id": employee[0],
        "username": employee[1],
        "role": "admin"
    }

    try:
        result = update_stock_quantity(
            product_id=101,
            new_quantity=15,
            approved_by=forged_employee
        )

        print("TEST FAILED:", result)

    except PermissionError as error:
        print("\nTEST PASSED!")
        print("Unauthorized approval blocked:", error)
