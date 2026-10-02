import sqlite3
import pandas as pd
from pathlib import Path


# -------------------------------------------------
# PATHS
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"
DB_PATH = Path(__file__).resolve().parent / "access_control.db"


# -------------------------------------------------
# CREATE DATABASE CONNECTION
# -------------------------------------------------
def get_connection():
    """Create and return a SQLite database connection."""
    return sqlite3.connect(DB_PATH)


# -------------------------------------------------
# LOAD CSV DATA INTO SQLITE
# -------------------------------------------------
def create_database():
    """Create SQLite tables from the project's CSV files."""

    conn = get_connection()

    csv_files = {
        "users": "users.csv",
        "roles": "roles.csv",
        "permissions": "permissions.csv",
        "resources": "resources.csv",
        "user_roles": "user_roles.csv",
        "role_permissions": "role_permissions.csv",
        "permission_resources": "permission_resources.csv",
    }

    print("\nCreating SQLite database...")

    for table_name, file_name in csv_files.items():
        file_path = DATA_DIR / file_name

        if file_path.exists():
            df = pd.read_csv(file_path)

            df.to_sql(
                table_name,
                conn,
                if_exists="replace",
                index=False
            )

            print(f"Loaded {len(df)} records into table: {table_name}")
        else:
            print(f"WARNING: File not found: {file_path}")

    conn.close()
    print("\nSQLite database created successfully!")
    print(f"Database location: {DB_PATH}")


# -------------------------------------------------
# SQL QUERIES FOR ACCESS CONTROL ANALYSIS
# -------------------------------------------------
def run_sql_analysis():
    """Run SQL queries against the access control database."""

    conn = get_connection()

    print("\n" + "=" * 60)
    print("SQL ACCESS CONTROL ANALYSIS")
    print("=" * 60)

    # Query 1: Count users
    total_users = pd.read_sql_query(
        "SELECT COUNT(*) AS total_users FROM users",
        conn
    )

    print("\n1. TOTAL USERS")
    print(total_users.to_string(index=False))

    # Query 2: Count roles
    total_roles = pd.read_sql_query(
        "SELECT COUNT(*) AS total_roles FROM roles",
        conn
    )

    print("\n2. TOTAL ROLES")
    print(total_roles.to_string(index=False))

    # Query 3: Count permissions
    total_permissions = pd.read_sql_query(
        "SELECT COUNT(*) AS total_permissions FROM permissions",
        conn
    )

    print("\n3. TOTAL PERMISSIONS")
    print(total_permissions.to_string(index=False))

    # Query 4: Users with the most role assignments
    user_role_counts = pd.read_sql_query(
        """
        SELECT
            user_id,
            COUNT(role_id) AS role_count
        FROM user_roles
        GROUP BY user_id
        ORDER BY role_count DESC
        LIMIT 10
        """,
        conn
    )

    print("\n4. TOP USERS BY NUMBER OF ROLES")
    print(user_role_counts.to_string(index=False))

    # Query 5: Roles with the most permissions
    role_permission_counts = pd.read_sql_query(
        """
        SELECT
            role_id,
            COUNT(permission_id) AS permission_count
        FROM role_permissions
        GROUP BY role_id
        ORDER BY permission_count DESC
        LIMIT 10
        """,
        conn
    )

    print("\n5. TOP ROLES BY NUMBER OF PERMISSIONS")
    print(role_permission_counts.to_string(index=False))

    conn.close()

    print("\nSQL analysis completed successfully!")


# -------------------------------------------------
# RUN DATABASE + SQL ANALYSIS
# -------------------------------------------------
if __name__ == "__main__":
    create_database()
    run_sql_analysis()