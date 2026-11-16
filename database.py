
import sqlite3
from pathlib import Path

# Get the project folder location
BASE_DIR = Path(__file__).parent

# Database file location
DATABASE_PATH = BASE_DIR / "inventory.db"


def get_database_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    return connection

if __name__ == "__main__":
    connection = get_database_connection()

    print("Database connection successful!")

    connection.close()
