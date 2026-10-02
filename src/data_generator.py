import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# ============================================================
# ACCESS CONTROL / PRIVILEGE ANALYSIS
# REALISTIC ENTERPRISE DATASET GENERATOR
# ============================================================

# Reproducibility
random.seed(42)
np.random.seed(42)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

os.makedirs(RAW_DATA_DIR, exist_ok=True)


# ============================================================
# CONFIGURATION
# ============================================================

NUM_USERS = 300

DEPARTMENTS = [
    "Information Technology",
    "Finance",
    "Human Resources",
    "Sales",
    "Marketing",
    "Operations",
    "Legal",
    "Executive",
    "Security",
    "Engineering",
    "Customer Support"
]

DEPARTMENT_LOCATIONS = {
    "Information Technology": ["New York", "Austin", "Chicago"],
    "Finance": ["New York", "Chicago", "Boston"],
    "Human Resources": ["New York", "Atlanta", "Chicago"],
    "Sales": ["New York", "Dallas", "Denver", "Los Angeles"],
    "Marketing": ["New York", "Los Angeles", "Chicago"],
    "Operations": ["Chicago", "Dallas", "Atlanta"],
    "Legal": ["New York", "Washington DC", "Chicago"],
    "Executive": ["New York"],
    "Security": ["New York", "Austin", "Washington DC"],
    "Engineering": ["Austin", "Seattle", "New York"],
    "Customer Support": ["Denver", "Atlanta", "Dallas"]
}

FIRST_NAMES = [
    "James", "John", "Robert", "Michael", "William",
    "David", "Richard", "Joseph", "Thomas", "Daniel",
    "Matthew", "Anthony", "Mark", "Donald", "Steven",
    "Paul", "Andrew", "Joshua", "Kenneth", "Kevin",
    "Emily", "Olivia", "Sophia", "Emma", "Ava",
    "Mia", "Isabella", "Charlotte", "Amelia", "Harper",
    "Evelyn", "Abigail", "Ella", "Scarlett", "Grace",
    "Chloe", "Victoria", "Hannah", "Natalie", "Samantha"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones",
    "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris",
    "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"
]


# ============================================================
# ROLES
# ============================================================

ROLES = [
    {
        "role_id": "R001",
        "role_name": "IT Support Analyst",
        "department": "Information Technology",
        "role_risk": "Medium"
    },
    {
        "role_id": "R002",
        "role_name": "System Administrator",
        "department": "Information Technology",
        "role_risk": "High"
    },
    {
        "role_id": "R003",
        "role_name": "Database Administrator",
        "department": "Information Technology",
        "role_risk": "Critical"
    },
    {
        "role_id": "R004",
        "role_name": "Security Analyst",
        "department": "Security",
        "role_risk": "High"
    },
    {
        "role_id": "R005",
        "role_name": "Security Administrator",
        "department": "Security",
        "role_risk": "Critical"
    },
    {
        "role_id": "R006",
        "role_name": "Financial Analyst",
        "department": "Finance",
        "role_risk": "Medium"
    },
    {
        "role_id": "R007",
        "role_name": "Finance Manager",
        "department": "Finance",
        "role_risk": "High"
    },
    {
        "role_id": "R008",
        "role_name": "Payroll Specialist",
        "department": "Finance",
        "role_risk": "High"
    },
    {
        "role_id": "R009",
        "role_name": "HR Specialist",
        "department": "Human Resources",
        "role_risk": "Medium"
    },
    {
        "role_id": "R010",
        "role_name": "HR Manager",
        "department": "Human Resources",
        "role_risk": "High"
    },
    {
        "role_id": "R011",
        "role_name": "Sales Representative",
        "department": "Sales",
        "role_risk": "Low"
    },
    {
        "role_id": "R012",
        "role_name": "Sales Manager",
        "department": "Sales",
        "role_risk": "Medium"
    },
    {
        "role_id": "R013",
        "role_name": "Marketing Analyst",
        "department": "Marketing",
        "role_risk": "Low"
    },
    {
        "role_id": "R014",
        "role_name": "Marketing Manager",
        "department": "Marketing",
        "role_risk": "Medium"
    },
    {
        "role_id": "R015",
        "role_name": "Operations Analyst",
        "department": "Operations",
        "role_risk": "Medium"
    },
    {
        "role_id": "R016",
        "role_name": "Operations Manager",
        "department": "Operations",
        "role_risk": "High"
    },
    {
        "role_id": "R017",
        "role_name": "Legal Counsel",
        "department": "Legal",
        "role_risk": "High"
    },
    {
        "role_id": "R018",
        "role_name": "Executive Manager",
        "department": "Executive",
        "role_risk": "Critical"
    },
    {
        "role_id": "R019",
        "role_name": "Software Engineer",
        "department": "Engineering",
        "role_risk": "Medium"
    },
    {
        "role_id": "R020",
        "role_name": "Engineering Manager",
        "department": "Engineering",
        "role_risk": "High"
    },
    {
        "role_id": "R021",
        "role_name": "Customer Support Agent",
        "department": "Customer Support",
        "role_risk": "Low"
    },
    {
        "role_id": "R022",
        "role_name": "Customer Support Manager",
        "department": "Customer Support",
        "role_risk": "Medium"
    },
    {
        "role_id": "R023",
        "role_name": "Read Only Auditor",
        "department": "Security",
        "role_risk": "Low"
    },
    {
        "role_id": "R024",
        "role_name": "Privileged Access Administrator",
        "department": "Information Technology",
        "role_risk": "Critical"
    }
]


# ============================================================
# RESOURCES
# ============================================================

RESOURCES = [
    {
        "resource_id": "RES001",
        "resource_name": "Active Directory",
        "resource_type": "Identity System",
        "classification": "Restricted"
    },
    {
        "resource_id": "RES002",
        "resource_name": "Production Database",
        "resource_type": "Database",
        "classification": "Restricted"
    },
    {
        "resource_id": "RES003",
        "resource_name": "Financial Database",
        "resource_type": "Database",
        "classification": "Confidential"
    },
    {
        "resource_id": "RES004",
        "resource_name": "Payroll System",
        "resource_type": "Application",
        "classification": "Restricted"
    },
    {
        "resource_id": "RES005",
        "resource_name": "HR Management System",
        "resource_type": "Application",
        "classification": "Confidential"
    },
    {
        "resource_id": "RES006",
        "resource_name": "Customer CRM",
        "resource_type": "Application",
        "classification": "Confidential"
    },
    {
        "resource_id": "RES007",
        "resource_name": "Security Information Platform",
        "resource_type": "Security Platform",
        "classification": "Restricted"
    },
    {
        "resource_id": "RES008",
        "resource_name": "Source Code Repository",
        "resource_type": "Development Platform",
        "classification": "Confidential"
    },
    {
        "resource_id": "RES009",
        "resource_name": "Cloud Management Console",
        "resource_type": "Cloud Platform",
        "classification": "Restricted"
    },
    {
        "resource_id": "RES010",
        "resource_name": "Marketing Analytics Platform",
        "resource_type": "Analytics Platform",
        "classification": "Internal"
    },
    {
        "resource_id": "RES011",
        "resource_name": "Sales Reporting Platform",
        "resource_type": "Analytics Platform",
        "classification": "Internal"
    },
    {
        "resource_id": "RES012",
        "resource_name": "Legal Document Repository",
        "resource_type": "Document System",
        "classification": "Confidential"
    },
    {
        "resource_id": "RES013",
        "resource_name": "Operations Management System",
        "resource_type": "Application",
        "classification": "Internal"
    },
    {
        "resource_id": "RES014",
        "resource_name": "Customer Support Portal",
        "resource_type": "Application",
        "classification": "Internal"
    },
    {
        "resource_id": "RES015",
        "resource_name": "Enterprise Data Warehouse",
        "resource_type": "Database",
        "classification": "Restricted"
    }
]


# ============================================================
# PERMISSIONS
# ============================================================

PERMISSIONS = [
    {
        "permission_id": "P001",
        "permission_name": "View User Accounts",
        "access_type": "Read",
        "sensitivity": "Medium",
        "resource_id": "RES001"
    },
    {
        "permission_id": "P002",
        "permission_name": "Create User Accounts",
        "access_type": "Write",
        "sensitivity": "High",
        "resource_id": "RES001"
    },
    {
        "permission_id": "P003",
        "permission_name": "Modify User Accounts",
        "access_type": "Admin",
        "sensitivity": "Critical",
        "resource_id": "RES001"
    },
    {
        "permission_id": "P004",
        "permission_name": "Delete User Accounts",
        "access_type": "Admin",
        "sensitivity": "Critical",
        "resource_id": "RES001"
    },
    {
        "permission_id": "P005",
        "permission_name": "View Production Database",
        "access_type": "Read",
        "sensitivity": "High",
        "resource_id": "RES002"
    },
    {
        "permission_id": "P006",
        "permission_name": "Modify Production Database",
        "access_type": "Write",
        "sensitivity": "Critical",
        "resource_id": "RES002"
    },
    {
        "permission_id": "P007",
        "permission_name": "Administer Production Database",
        "access_type": "Admin",
        "sensitivity": "Critical",
        "resource_id": "RES002"
    },
    {
        "permission_id": "P008",
        "permission_name": "View Financial Records",
        "access_type": "Read",
        "sensitivity": "High",
        "resource_id": "RES003"
    },
    {
        "permission_id": "P009",
        "permission_name": "Modify Financial Records",
        "access_type": "Write",
        "sensitivity": "Critical",
        "resource_id": "RES003"
    },
    {
        "permission_id": "P010",
        "permission_name": "Approve Financial Transactions",
        "access_type": "Approve",
        "sensitivity": "Critical",
        "resource_id": "RES003"
    },
    {
        "permission_id": "P011",
        "permission_name": "View Payroll",
        "access_type": "Read",
        "sensitivity": "High",
        "resource_id": "RES004"
    },
    {
        "permission_id": "P012",
        "permission_name": "Modify Payroll",
        "access_type": "Write",
        "sensitivity": "Critical",
        "resource_id": "RES004"
    },
    {
        "permission_id": "P013",
        "permission_name": "Approve Payroll",
        "access_type": "Approve",
        "sensitivity": "Critical",
        "resource_id": "RES004"
    },
    {
        "permission_id": "P014",
        "permission_name": "View Employee Records",
        "access_type": "Read",
        "sensitivity": "High",
        "resource_id": "RES005"
    },
    {
        "permission_id": "P015",
        "permission_name": "Modify Employee Records",
        "access_type": "Write",
        "sensitivity": "High",
        "resource_id": "RES005"
    },
    {
        "permission_id": "P016",
        "permission_name": "View Customer Records",
        "access_type": "Read",
        "sensitivity": "Medium",
        "resource_id": "RES006"
    },
    {
        "permission_id": "P017",
        "permission_name": "Modify Customer Records",
        "access_type": "Write",
        "sensitivity": "High",
        "resource_id": "RES006"
    },
    {
        "permission_id": "P018",
        "permission_name": "View Security Logs",
        "access_type": "Read",
        "sensitivity": "High",
        "resource_id": "RES007"
    },
    {
        "permission_id": "P019",
        "permission_name": "Modify Security Rules",
        "access_type": "Admin",
        "sensitivity": "Critical",
        "resource_id": "RES007"
    },
    {
        "permission_id": "P020",
        "permission_name": "View Source Code",
        "access_type": "Read",
        "sensitivity": "Medium",
        "resource_id": "RES008"
    },
    {
        "permission_id": "P021",
        "permission_name": "Modify Source Code",
        "access_type": "Write",
        "sensitivity": "High",
        "resource_id": "RES008"
    },
    {
        "permission_id": "P022",
        "permission_name": "Deploy Production Code",
        "access_type": "Deploy",
        "sensitivity": "Critical",
        "resource_id": "RES008"
    },
    {
        "permission_id": "P023",
        "permission_name": "View Cloud Resources",
        "access_type": "Read",
        "sensitivity": "High",
        "resource_id": "RES009"
    },
    {
        "permission_id": "P024",
        "permission_name": "Modify Cloud Resources",
        "access_type": "Admin",
        "sensitivity": "Critical",
        "resource_id": "RES009"
    },
    {
        "permission_id": "P025",
        "permission_name": "View Marketing Analytics",
        "access_type": "Read",
        "sensitivity": "Low",
        "resource_id": "RES010"
    },
    {
        "permission_id": "P026",
        "permission_name": "Modify Marketing Campaigns",
        "access_type": "Write",
        "sensitivity": "Medium",
        "resource_id": "RES010"
    },
    {
        "permission_id": "P027",
        "permission_name": "View Sales Reports",
        "access_type": "Read",
        "sensitivity": "Low",
        "resource_id": "RES011"
    },
    {
        "permission_id": "P028",
        "permission_name": "Modify Sales Reports",
        "access_type": "Write",
        "sensitivity": "Medium",
        "resource_id": "RES011"
    },
    {
        "permission_id": "P029",
        "permission_name": "View Legal Documents",
        "access_type": "Read",
        "sensitivity": "High",
        "resource_id": "RES012"
    },
    {
        "permission_id": "P030",
        "permission_name": "Modify Legal Documents",
        "access_type": "Write",
        "sensitivity": "High",
        "resource_id": "RES012"
    },
    {
        "permission_id": "P031",
        "permission_name": "View Operations Data",
        "access_type": "Read",
        "sensitivity": "Medium",
        "resource_id": "RES013"
    },
    {
        "permission_id": "P032",
        "permission_name": "Modify Operations Data",
        "access_type": "Write",
        "sensitivity": "High",
        "resource_id": "RES013"
    },
    {
        "permission_id": "P033",
        "permission_name": "View Support Tickets",
        "access_type": "Read",
        "sensitivity": "Low",
        "resource_id": "RES014"
    },
    {
        "permission_id": "P034",
        "permission_name": "Modify Support Tickets",
        "access_type": "Write",
        "sensitivity": "Medium",
        "resource_id": "RES014"
    },
    {
        "permission_id": "P035",
        "permission_name": "View Enterprise Data Warehouse",
        "access_type": "Read",
        "sensitivity": "High",
        "resource_id": "RES015"
    },
    {
        "permission_id": "P036",
        "permission_name": "Modify Enterprise Data Warehouse",
        "access_type": "Write",
        "sensitivity": "Critical",
        "resource_id": "RES015"
    }
]


# ============================================================
# ROLE-PERMISSION MAPPING
# ============================================================

ROLE_PERMISSION_MAP = {
    "R001": ["P001", "P002", "P018"],
    "R002": ["P001", "P002", "P003", "P005", "P018", "P023"],
    "R003": ["P005", "P006", "P007", "P035", "P036"],
    "R004": ["P018", "P020", "P023", "P035"],
    "R005": ["P001", "P002", "P003", "P018", "P019", "P023", "P024"],
    "R006": ["P008", "P027", "P035"],
    "R007": ["P008", "P009", "P010", "P011", "P035"],
    "R008": ["P011", "P012"],
    "R009": ["P014", "P015"],
    "R010": ["P014", "P015", "P011"],
    "R011": ["P016", "P027"],
    "R012": ["P016", "P017", "P027", "P028"],
    "R013": ["P025", "P026"],
    "R014": ["P025", "P026", "P035"],
    "R015": ["P031", "P032", "P035"],
    "R016": ["P031", "P032", "P035", "P036"],
    "R017": ["P029", "P030", "P035"],
    "R018": ["P008", "P010", "P014", "P016", "P023", "P035"],
    "R019": ["P020", "P021", "P025"],
    "R020": ["P020", "P021", "P022", "P023", "P035"],
    "R021": ["P016", "P033", "P034"],
    "R022": ["P016", "P017", "P033", "P034"],
    "R023": ["P001", "P005", "P008", "P014", "P018", "P020", "P023", "P035"],
    "R024": [
        "P001", "P002", "P003", "P004",
        "P005", "P007",
        "P018", "P019",
        "P023", "P024"
    ]
}


# ============================================================
# GENERATE USERS
# ============================================================

def generate_users():
    users = []
    used_usernames = set()

    for i in range(1, NUM_USERS + 1):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)

        base_username = f"{first_name.lower()[0]}{last_name.lower()}"

        username = base_username
        counter = 1

        while username in used_usernames:
            username = f"{base_username}{counter}"
            counter += 1

        used_usernames.add(username)

        department = random.choice(DEPARTMENTS)
        location = random.choice(DEPARTMENT_LOCATIONS[department])

        department_roles = [
            role for role in ROLES
            if role["department"] == department
        ]

        if not department_roles:
            department_roles = ROLES

        primary_role = random.choice(department_roles)

        status = random.choices(
            ["Active", "Inactive", "Suspended"],
            weights=[0.88, 0.08, 0.04]
        )[0]

        hire_date = datetime.now() - timedelta(
            days=random.randint(30, 3650)
        )

        users.append({
            "user_id": f"U{i:04d}",
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "department": department,
            "location": location,
            "job_title": primary_role["role_name"],
            "status": status,
            "hire_date": hire_date.date()
        })

    return pd.DataFrame(users)


# ============================================================
# GENERATE USER-ROLE MAPPINGS
# ============================================================

def generate_user_roles(users_df):
    mappings = []

    role_lookup = {
        role["role_id"]: role
        for role in ROLES
    }

    for _, user in users_df.iterrows():

        primary_roles = [
            role for role in ROLES
            if (
                role["department"] == user["department"]
                and role["role_name"] == user["job_title"]
            )
        ]

        if primary_roles:
            primary_role = primary_roles[0]
        else:
            primary_role = random.choice(ROLES)

        mappings.append({
            "user_id": user["user_id"],
            "role_id": primary_role["role_id"],
            "assignment_type": "Primary",
            "assigned_date": user["hire_date"]
        })

        # Some users receive additional access roles.
        if random.random() < 0.18:
            eligible_roles = [
                role for role in ROLES
                if role["role_id"] != primary_role["role_id"]
            ]

            extra_role = random.choice(eligible_roles)

            mappings.append({
                "user_id": user["user_id"],
                "role_id": extra_role["role_id"],
                "assignment_type": "Additional",
                "assigned_date": (
                    datetime.now()
                    - timedelta(days=random.randint(1, 1000))
                ).date()
            })

    # Intentionally create a few over-privileged accounts.
    high_risk_users = random.sample(
        users_df["user_id"].tolist(),
        12
    )

    privileged_roles = [
        "R002",
        "R003",
        "R005",
        "R007",
        "R018",
        "R024"
    ]

    for user_id in high_risk_users:

        existing_roles = {
            mapping["role_id"]
            for mapping in mappings
            if mapping["user_id"] == user_id
        }

        number_of_extra_roles = random.randint(2, 4)

        available_roles = [
            role_id
            for role_id in privileged_roles
            if role_id not in existing_roles
        ]

        selected_roles = random.sample(
            available_roles,
            min(number_of_extra_roles, len(available_roles))
        )

        for role_id in selected_roles:
            mappings.append({
                "user_id": user_id,
                "role_id": role_id,
                "assignment_type": "Privileged",
                "assigned_date": (
                    datetime.now()
                    - timedelta(days=random.randint(1, 500))
                ).date()
            })

    return pd.DataFrame(mappings)


# ============================================================
# GENERATE ROLE-PERMISSION MAPPINGS
# ============================================================

def generate_role_permissions():
    mappings = []

    for role_id, permissions in ROLE_PERMISSION_MAP.items():
        for permission_id in permissions:

            mappings.append({
                "role_id": role_id,
                "permission_id": permission_id,
                "assignment_source": "Role Based Access Control"
            })

    return pd.DataFrame(mappings)


# ============================================================
# GENERATE PERMISSION-RESOURCE MAPPINGS
# ============================================================

def generate_permission_resources():
    mappings = []

    for permission in PERMISSIONS:
        mappings.append({
            "permission_id": permission["permission_id"],
            "resource_id": permission["resource_id"]
        })

    return pd.DataFrame(mappings)


# ============================================================
# CREATE DATAFRAMES
# ============================================================

def create_datasets():

    print("=" * 60)
    print("ACCESS CONTROL / PRIVILEGE ANALYSIS")
    print("Generating realistic enterprise dataset...")
    print("=" * 60)

    users_df = generate_users()

    roles_df = pd.DataFrame(ROLES)

    permissions_df = pd.DataFrame(PERMISSIONS)

    resources_df = pd.DataFrame(RESOURCES)

    user_roles_df = generate_user_roles(users_df)

    role_permissions_df = generate_role_permissions()

    permission_resources_df = generate_permission_resources()

    # Save all datasets.
    datasets = {
        "users.csv": users_df,
        "roles.csv": roles_df,
        "permissions.csv": permissions_df,
        "resources.csv": resources_df,
        "user_roles.csv": user_roles_df,
        "role_permissions.csv": role_permissions_df,
        "permission_resources.csv": permission_resources_df
    }

    for filename, dataframe in datasets.items():

        file_path = os.path.join(
            RAW_DATA_DIR,
            filename
        )

        dataframe.to_csv(
            file_path,
            index=False
        )

        print(
            f"Created: {filename} "
            f"({len(dataframe):,} records)"
        )

    print("=" * 60)
    print("DATASET GENERATION COMPLETE")
    print(f"Location: {RAW_DATA_DIR}")
    print("=" * 60)

    print("\nDataset Summary:")
    print(f"Users: {len(users_df):,}")
    print(f"Roles: {len(roles_df):,}")
    print(f"Permissions: {len(permissions_df):,}")
    print(f"Resources: {len(resources_df):,}")
    print(f"User-Role Relationships: {len(user_roles_df):,}")
    print(
        f"Role-Permission Relationships: "
        f"{len(role_permissions_df):,}"
    )
    print(
        f"Permission-Resource Relationships: "
        f"{len(permission_resources_df):,}"
    )


# ============================================================
# RUN SCRIPT
# ============================================================

if __name__ == "__main__":
    create_datasets()