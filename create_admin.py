
from user_management import create_user

username = input("Enter admin username: ")
password = input("Enter admin password: ")

result = create_user(
    username=username,
    password=password,
    role="admin"
)

print(result)
