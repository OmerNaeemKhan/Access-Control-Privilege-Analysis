# Access Control & Privilege Analysis

## Project Overview

The Access Control & Privilege Analysis project is a cybersecurity and data analytics application designed to analyze users, roles, permissions, and resources within an access control environment.

The project identifies potential security risks such as:

- Excessive permissions
- Excessive roles
- High-privilege roles
- Unusual privilege assignments
- Access anomalies
- Role and permission distribution patterns

The application combines **Python, SQL, Artificial Intelligence, and an interactive dashboard** to provide a complete security analysis workflow.

---

# Project Requirements Covered

This project includes the following required components:

## 1. Interactive Dashboard

An interactive Streamlit dashboard provides a visual overview of the access control environment.

The dashboard includes:

- Total Users
- Total Roles
- Total Permissions
- Total Resources
- Excessive Permissions
- Excessive Roles
- High-Privilege Roles
- Total Security Findings
- User Analysis
- Role Analysis
- Security Findings
- Data Explorer
- SQL Analysis Results

The dashboard allows users to explore security data and findings in an organized and user-friendly interface.

---

## 2. Artificial Intelligence Models

The project uses multiple AI and machine learning techniques.

### Isolation Forest

Isolation Forest is used for:

- Anomaly detection
- Identifying unusual privilege assignments
- Detecting users with potentially abnormal access patterns

This helps identify users whose access behavior differs significantly from the rest of the environment.

### K-Means Clustering

K-Means clustering is used for:

- Privilege pattern clustering
- Grouping users based on access characteristics
- Identifying similar privilege patterns
- Detecting potentially unusual clusters

These AI models provide additional insight beyond traditional rule-based security analysis.

---

## 3. SQL Database Analysis

The project uses a SQLite database to store and analyze access control data.

The SQL database includes information related to:

- Users
- Roles
- Permissions
- Resources
- User-role assignments
- Role-permission assignments
- Permission-resource relationships

SQL queries are used to perform analysis such as:

- SELECT queries
- COUNT queries
- GROUP BY queries
- ORDER BY queries
- Role permission analysis
- Access data aggregation

The application displays SQL analysis results in the dashboard.

Example analysis includes:

- Total users
- Total roles
- Total permissions
- Total resources
- Top roles by number of permissions

---

## 4. Python Analysis

Python is used as the main programming language for the project.

Python performs:

- Data loading
- Data cleaning
- Data processing
- Access control analysis
- Security finding generation
- CSV processing
- Database creation
- SQL execution
- AI and machine learning analysis
- Output generation
- Dashboard integration

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming and data analysis |
| Pandas | Data processing and CSV analysis |
| SQLite | Database storage and SQL analysis |
| Scikit-learn | Machine learning and AI models |
| Isolation Forest | Anomaly detection |
| K-Means | Privilege pattern clustering |
| Streamlit | Interactive dashboard |
| CSV | Source access control datasets |

---

# Project Structure

```text
Access_Control_Privilege_Analysis/
│
├── .venv/
│
├── dashboard/
│   ├── app.py
│   ├── ai_privilege_analysis.py
│   └── outputs/
│
├── data/
│   ├── raw/
│   │   ├── users.csv
│   │   ├── roles.csv
│   │   ├── permissions.csv
│   │   ├── resources.csv
│   │   ├── user_roles.csv
│   │   ├── role_permissions.csv
│   │   └── permission_resources.csv
│   │
│   └── processed/
│
├── database/
│   ├── access_control.db
│   └── sql_database.py
│
├── outputs/
│   ├── charts/
│   ├── findings/
│   ├── graph_visualizations/
│   ├── excessive_permissions.csv
│   ├── excessive_roles.csv
│   ├── high_privilege_roles.csv
│   ├── role_privilege_distribution.csv
│   ├── user_permission_distribution.csv
│   └── user_role_distribution.csv
│
├── setup.py
│
└── README.md

Dataset

The project analyzes an access control dataset containing approximately:

300 Users
24 Roles
36 Permissions
15 Resources

The datasets represent relationships between users, roles, permissions, and resources.

The main source files include:

users.csv

Contains information about system users.

roles.csv

Contains available access control roles.

permissions.csv

Contains available permissions.

resources.csv

Contains protected system resources.

user_roles.csv

Maps users to their assigned roles.

role_permissions.csv

Maps roles to their assigned permissions.

permission_resources.csv

Maps permissions to resources.

Security Analysis

The project performs multiple types of security analysis.

Excessive Permissions

The application identifies users who have more permissions than expected or required.

Potential risks include:

Overprivileged accounts
Excessive access rights
Violation of the principle of least privilege
Excessive Roles

The application identifies users assigned to an unusually high number of roles.

Potential risks include:

Role accumulation
Privilege creep
Unnecessary access expansion
High-Privilege Roles

The application identifies roles with a high number of assigned permissions.

These roles may require additional monitoring because compromise of a highly privileged account could create significant security risk.

Anomaly Detection

Isolation Forest is used to identify unusual access patterns.

Examples may include users with:

Unusually high permission counts
Unusually high role counts
Access patterns significantly different from other users
Privilege Pattern Clustering

K-Means clustering groups users with similar privilege characteristics.

This helps identify:

Normal access groups
Similar user privilege patterns
Outliers or unusual clusters
Running the Project
Step 1: Open the Project

Open the project folder in Visual Studio Code.

Access_Control_Privilege_Analysis
Step 2: Activate the Virtual Environment

In PowerShell:

.\.venv\Scripts\Activate.ps1
Step 3: Install Required Libraries

If required, install the dependencies:

python -m pip install pandas scikit-learn streamlit
Step 4: Run the Python and AI Analysis

Run the AI privilege analysis:

python .\dashboard\ai_privilege_analysis.py

The analysis uses:

Isolation Forest for anomaly detection
K-Means for privilege pattern clustering

Successful execution should display:

AI MODELS USED:

1. Isolation Forest - Anomaly Detection
2. K-Means - Privilege Pattern Clustering

Analysis completed successfully.
Step 5: Run the SQL Database Analysis

Run the SQL analysis:

python .\database\sql_database.py

This creates and analyzes the SQLite database.

The analysis performs SQL operations including:

SELECT
COUNT
GROUP BY
ORDER BY

Successful execution should display:

SQL analysis completed successfully!
Step 6: Start the Dashboard

Run the Streamlit application:

streamlit run .\dashboard\app.py

The dashboard should open in the browser.

Default local address:

http://localhost:8502
Dashboard Features

The Streamlit dashboard contains the following sections.

Dashboard Overview

Displays high-level access control statistics.

Examples include:

Total Users
Total Roles
Total Permissions
Total Resources
User Analysis

Provides analysis related to users and their access patterns.

Examples include:

User role distribution
User permission distribution
Excessive permissions
Potential anomalies
Role Analysis

Provides analysis related to roles and assigned privileges.

Examples include:

Role privilege distribution
High-privilege roles
Top roles by permission count
Excessive role analysis
Security Findings

Displays identified security risks and findings.

Examples include:

Excessive Permissions
Excessive Roles
High-Privilege Roles
Total Open Findings
Data Explorer

Allows exploration of the analyzed access control datasets and results.

SQL Analysis

Displays results generated using the SQLite database and SQL queries.

Examples include:

SQL Users
SQL Roles
SQL Permissions
SQL Resources
Top Roles by Permission Count

The SQL database connection and query results demonstrate the use of structured database analysis in the project.

AI Models Used
Model 1: Isolation Forest

Purpose: Anomaly Detection

Isolation Forest is used to detect unusual access and privilege patterns.

Possible features analyzed include:

Number of roles assigned to a user
Number of permissions assigned
Privilege-related characteristics

Users with unusual patterns can be flagged for further security review.

Model 2: K-Means Clustering

Purpose: Privilege Pattern Clustering

K-Means groups users with similar access characteristics.

The model helps identify:

Groups with similar privileges
Common access patterns
Users that do not fit expected patterns
SQL Analysis

The project uses SQLite to demonstrate database and SQL skills.

The database file is:

database/access_control.db

The SQL analysis script is:

database/sql_database.py

The script creates database tables, loads the access control data, and runs analytical queries.

Example SQL concepts demonstrated include:

SELECT * FROM users;
SELECT COUNT(*) FROM users;
SELECT role_id, COUNT(permission_id)
FROM role_permissions
GROUP BY role_id
ORDER BY COUNT(permission_id) DESC;

These queries help analyze the structure and distribution of privileges across the environment.

Project Workflow

The overall project workflow is:

Raw CSV Access Control Data
            ↓
      Python Processing
            ↓
     Security Analysis
            ↓
      Output CSV Files
            ↓
    SQLite Database Creation
            ↓
        SQL Analysis
            ↓
       AI/ML Analysis
       ├── Isolation Forest
       └── K-Means Clustering
            ↓
    Streamlit Dashboard
            ↓
 Interactive Security Insights
Key Cybersecurity Concepts

This project demonstrates several important cybersecurity concepts.

Principle of Least Privilege

Users should only receive the minimum permissions required to perform their job functions.

The project identifies potentially excessive permissions that may violate this principle.

Role-Based Access Control

The project analyzes a Role-Based Access Control environment where access is managed through relationships between:

Users
  ↓
Roles
  ↓
Permissions
  ↓
Resources
Privilege Creep

Privilege creep occurs when users gradually accumulate unnecessary access rights.

The project helps identify users with excessive roles or permissions.

Anomaly Detection

Machine learning is used to identify access patterns that differ from normal behavior.

This provides an additional layer of analysis beyond traditional threshold-based security checks.

Results

The project successfully demonstrates integration of four major technical requirements:

Interactive Dashboard

A Streamlit-based dashboard provides visual access to security and access control findings.

Artificial Intelligence

Two different AI and machine learning techniques are used:

Isolation Forest
K-Means Clustering
SQL

SQLite and SQL queries are used for database storage and structured analysis.

Python

Python is used for data processing, security analysis, AI, database integration, and dashboard functionality.

Final Deliverables

The completed project includes:

Python source code
Access control CSV datasets
Security analysis outputs
AI anomaly detection
AI privilege pattern clustering
SQLite database
SQL analysis script
Interactive Streamlit dashboard
Security findings
README documentation
Conclusion

The Access Control & Privilege Analysis project demonstrates how cybersecurity access control data can be analyzed using a combination of Python, SQL, artificial intelligence, and interactive data visualization.

The application helps identify potential security issues such as excessive permissions, excessive roles, high-privilege roles, and unusual access patterns.

By combining traditional security analysis with SQL queries and machine learning models, the project provides a more comprehensive view of access control risk.

The final solution demonstrates practical skills in:

Cybersecurity
Access Control Analysis
RBAC
Python
SQL
SQLite
Data Analysis
Machine Learning
Anomaly Detection
Clustering
Dashboard Development
Security Visualization
