
from user_management import create_user

username = input("Enter regular username: ")
password = input("Enter regular user password: ")

result = create_user(
    username=username,
    password=password,
    role="user"
)

print(result)
