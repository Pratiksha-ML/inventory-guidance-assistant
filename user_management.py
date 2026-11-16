
from database import get_database_connection
from werkzeug.security import generate_password_hash, check_password_hash


def create_user(username, password, role="user"):

    if role not in ("admin", "user"):
        raise ValueError("Invalid user role.")

    password_hash = generate_password_hash(password)

    connection = get_database_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
            """,
            (username, password_hash, role)
        )

        connection.commit()
        return "User created successfully."

    except Exception:
        return "Username already exists or user creation failed."

    finally:
        connection.close()


def authenticate_user(username, password):

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT user_id, username, password_hash, role
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()
    connection.close()

    if user and check_password_hash(user[2], password):
        return {
            "user_id": user[0],
            "username": user[1],
            "role": user[3]
        }

    return None


def can_approve_stock(user):

    if not user:
        return False

    user_id = user.get("user_id")
    username = user.get("username")

    if not user_id or not username:
        return False

    connection = get_database_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT role
            FROM users
            WHERE user_id = ? AND username = ?
            """,
            (user_id, username)
        )

        result = cursor.fetchone()

        if result is None:
            return False

        return result[0] == "admin"

    finally:
        connection.close()
