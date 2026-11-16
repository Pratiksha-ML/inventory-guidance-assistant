
from user_management import authenticate_user

username = input("Enter username: ")
password = input("Enter password: ")

user = authenticate_user(username, password)

if user:
    print("\nLogin successful!")
    print("Username:", user["username"])
    print("Role:", user["role"])
else:
    print("\nInvalid username or password.")
