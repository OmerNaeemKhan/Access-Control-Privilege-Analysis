import sqlite3
from pathlib import Path
import pandas as pd


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "raw"
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "access_control.db"


# ============================================================
# CREATE DATABASE
# ============================================================

def create_database():
    """Create the SQLite database and load all CSV datasets."""

    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    # Remove the old database so every run starts fresh
    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()

    connection = sqlite3.connect(DATABASE_PATH)

    print("=" * 60)
    print("CREATING ACCESS CONTROL DATABASE")
    print("=" * 60)

    csv_files = {
        "users": "users.csv",
        "roles": "roles.csv",
        "permissions": "permissions.csv",
        "resources": "resources.csv",
        "user_roles": "user_roles.csv",
        "role_permissions": "role_permissions.csv",
        "permission_resources": "permission_resources.csv",
    }

    for table_name, file_name in csv_files.items():
        file_path = DATA_DIR / file_name

        dataframe = pd.read_csv(file_path)

        dataframe.to_sql(
            table_name,
            connection,
            if_exists="replace",
            index=False
        )

        print(f"Loaded {table_name}: {len(dataframe)} records")

    connection.close()

    print("\nDatabase created successfully!")
    print(f"Location: {DATABASE_PATH}")


# ============================================================
# RUN SCRIPT
# ============================================================

if __name__ == "__main__":
    create_database()