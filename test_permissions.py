
from user_management import authenticate_user, can_approve_stock

# Test regular user permissions
employee = authenticate_user(
    "employee1",
    input("Enter employee password: ")
)

print("\nREGULAR USER PERMISSION TEST")
print("----------------------------")

if employee:
    print("Login successful!")
    print("Role:", employee["role"])

    if can_approve_stock(employee):
        print("Employee can approve stock updates.")
    else:
        print("Employee cannot approve stock updates.")
else:
    print("Invalid username or password.")
