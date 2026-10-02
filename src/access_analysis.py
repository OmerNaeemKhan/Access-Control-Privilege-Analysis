import sqlite3
from pathlib import Path
import pandas as pd


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database" / "access_control.db"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """Connect to the access control database."""
    return sqlite3.connect(DATABASE_PATH)


# ============================================================
# ANALYSIS 1: USER ROLE DISTRIBUTION
# ============================================================

def analyze_user_roles(connection):
    """Identify users with an unusually high number of roles."""

    query = """
    SELECT
        u.user_id,
        u.username,
        u.department,
        COUNT(ur.role_id) AS role_count
    FROM users u
    JOIN user_roles ur
        ON u.user_id = ur.user_id
    GROUP BY
        u.user_id,
        u.username,
        u.department
    ORDER BY role_count DESC
    """

    dataframe = pd.read_sql_query(query, connection)

    average_roles = dataframe["role_count"].mean()
    threshold = average_roles * 2

    flagged = dataframe[
        dataframe["role_count"] > threshold
    ].copy()

    flagged["risk_reason"] = (
        "User has significantly more roles than average"
    )

    dataframe.to_csv(
        OUTPUT_DIR / "user_role_distribution.csv",
        index=False
    )

    flagged.to_csv(
        OUTPUT_DIR / "excessive_roles.csv",
        index=False
    )

    return dataframe, flagged, average_roles


# ============================================================
# ANALYSIS 2: EXCESSIVE PERMISSIONS
# ============================================================

def analyze_user_permissions(connection):
    """Identify users with unusually high effective permissions."""

    query = """
    SELECT
        u.user_id,
        u.username,
        u.department,
        COUNT(DISTINCT rp.permission_id) AS permission_count
    FROM users u
    JOIN user_roles ur
        ON u.user_id = ur.user_id
    JOIN role_permissions rp
        ON ur.role_id = rp.role_id
    GROUP BY
        u.user_id,
        u.username,
        u.department
    ORDER BY permission_count DESC
    """

    dataframe = pd.read_sql_query(query, connection)

    average_permissions = dataframe["permission_count"].mean()
    threshold = average_permissions * 1.75

    flagged = dataframe[
        dataframe["permission_count"] > threshold
    ].copy()

    flagged["risk_reason"] = (
        "User has significantly more permissions than average"
    )

    dataframe.to_csv(
        OUTPUT_DIR / "user_permission_distribution.csv",
        index=False
    )

    flagged.to_csv(
        OUTPUT_DIR / "excessive_permissions.csv",
        index=False
    )

    return dataframe, flagged, average_permissions


# ============================================================
# ANALYSIS 3: ROLE PRIVILEGE DISTRIBUTION
# ============================================================

def analyze_role_privileges(connection):
    """Identify roles with unusually high permission counts."""

    query = """
    SELECT
        r.role_id,
        r.role_name,
        r.department,
        COUNT(rp.permission_id) AS permission_count
    FROM roles r
    LEFT JOIN role_permissions rp
        ON r.role_id = rp.role_id
    GROUP BY
        r.role_id,
        r.role_name,
        r.department
    ORDER BY permission_count DESC
    """

    dataframe = pd.read_sql_query(query, connection)

    average_permissions = dataframe["permission_count"].mean()
    threshold = average_permissions * 1.75

    flagged = dataframe[
        dataframe["permission_count"] > threshold
    ].copy()

    flagged["risk_reason"] = (
        "Role contains significantly more permissions than average"
    )

    dataframe.to_csv(
        OUTPUT_DIR / "role_privilege_distribution.csv",
        index=False
    )

    flagged.to_csv(
        OUTPUT_DIR / "high_privilege_roles.csv",
        index=False
    )

    return dataframe, flagged, average_permissions


# ============================================================
# ANALYSIS 4: SENSITIVE PERMISSIONS
# ============================================================

def analyze_sensitive_permissions(connection):
    """Identify users with access to sensitive actions."""

    query = """
    SELECT DISTINCT
        u.user_id,
        u.username,
        u.department,
        r.role_name,
        p.permission_name,
        p.action,
        res.resource_name,
        res.resource_type
    FROM users u
    JOIN user_roles ur
        ON u.user_id = ur.user_id
    JOIN roles r
        ON ur.role_id = r.role_id
    JOIN role_permissions rp
        ON r.role_id = rp.role_id
    JOIN permissions p
        ON rp.permission_id = p.permission_id
    JOIN permission_resources pr
        ON p.permission_id = pr.permission_id
    JOIN resources res
        ON pr.resource_id = res.resource_id
    WHERE LOWER(p.action) IN (
        'delete',
        'modify',
        'admin',
        'write'
    )
    ORDER BY
        u.username,
        p.action
    """

    dataframe = pd.read_sql_query(query, connection)

    dataframe.to_csv(
        OUTPUT_DIR / "sensitive_permission_access.csv",
        index=False
    )

    return dataframe


# ============================================================
# MAIN ANALYSIS
# ============================================================

def run_analysis():

    print("=" * 65)
    print("ACCESS CONTROL & PRIVILEGE ANALYSIS")
    print("=" * 65)

    connection = get_connection()

    # User roles
    user_roles, excessive_roles, avg_roles = (
        analyze_user_roles(connection)
    )

    print(f"\nAverage roles per user: {avg_roles:.2f}")
    print(f"Users analyzed: {len(user_roles)}")
    print(
        f"Users flagged for excessive roles: "
        f"{len(excessive_roles)}"
    )

    # User permissions
    user_permissions, excessive_permissions, avg_permissions = (
        analyze_user_permissions(connection)
    )

    print(
        f"\nAverage effective permissions per user: "
        f"{avg_permissions:.2f}"
    )
    print(
        f"Users flagged for excessive permissions: "
        f"{len(excessive_permissions)}"
    )

    # Role privileges
    role_privileges, high_privilege_roles, avg_role_permissions = (
        analyze_role_privileges(connection)
    )

    print(
        f"\nAverage permissions per role: "
        f"{avg_role_permissions:.2f}"
    )
    print(
        f"High-privilege roles identified: "
        f"{len(high_privilege_roles)}"
    )

    # Sensitive permissions
    sensitive_permissions = analyze_sensitive_permissions(connection)

    print(
        f"\nSensitive permission assignments identified: "
        f"{len(sensitive_permissions)}"
    )

    connection.close()

    print("\n" + "=" * 65)
    print("ANALYSIS COMPLETE")
    print("=" * 65)
    print(f"\nResults saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    run_analysis()