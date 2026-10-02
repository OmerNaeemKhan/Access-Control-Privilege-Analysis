# ================================================================
# ACCESS CONTROL & PRIVILEGE ANALYSIS
# AI / MACHINE LEARNING PRIVILEGE RISK ANALYSIS
#
# AI MODEL 1: Isolation Forest
# Detects unusual user access and privilege patterns
#
# AI MODEL 2: K-Means Clustering
# Groups users into privilege-risk clusters
#
# OUTPUT:
# outputs/ai_user_risk_assessment.csv
# outputs/ai_anomaly_findings.csv
# outputs/ai_cluster_analysis.csv
# ================================================================

from pathlib import Path
import warnings

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")


# ================================================================
# PROJECT PATHS
# ================================================================

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data" / "raw"
OUTPUT_DIR = PROJECT_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)


# ================================================================
# HELPER FUNCTIONS
# ================================================================

def find_existing_file(possible_files):
    """
    Returns the first existing file from a list of possible paths.
    """

    for file_path in possible_files:
        if file_path.exists():
            return file_path

    return None


def find_column(df, possible_names):
    """
    Finds a matching column name regardless of capitalization.
    """

    normalized_columns = {
        column.lower().strip().replace(" ", "_"): column
        for column in df.columns
    }

    for name in possible_names:
        normalized_name = name.lower().strip().replace(" ", "_")

        if normalized_name in normalized_columns:
            return normalized_columns[normalized_name]

    return None


# ================================================================
# LOAD USER PERMISSION DATA
# ================================================================

print("\n" + "=" * 70)
print("AI PRIVILEGE ANALYSIS STARTED")
print("=" * 70)

permission_distribution_file = find_existing_file([
    OUTPUT_DIR / "user_permission_distribution.csv",
    OUTPUT_DIR / "findings" / "user_permission_distribution.csv"
])

if permission_distribution_file is None:
    raise FileNotFoundError(
        "\nCould not find user_permission_distribution.csv.\n"
        "Please make sure access_analysis.py has been run first.\n"
        "Expected location:\n"
        f"{OUTPUT_DIR / 'user_permission_distribution.csv'}"
    )

print(f"\nLoading user permission data from:")
print(permission_distribution_file)

permissions_df = pd.read_csv(permission_distribution_file)

print(f"\nPermission records loaded: {len(permissions_df)}")
print(f"Columns found: {list(permissions_df.columns)}")


# ================================================================
# IDENTIFY USER AND PERMISSION COLUMNS
# ================================================================

username_column = find_column(
    permissions_df,
    [
        "username",
        "user_name",
        "user",
        "name"
    ]
)

permission_count_column = find_column(
    permissions_df,
    [
        "permission_count",
        "permissions",
        "permissioncount",
        "count"
    ]
)

if username_column is None:
    raise ValueError(
        "\nCould not identify the username column in "
        "user_permission_distribution.csv."
    )

if permission_count_column is None:
    raise ValueError(
        "\nCould not identify the permission count column in "
        "user_permission_distribution.csv."
    )


# ================================================================
# CREATE BASE AI DATASET
# ================================================================

ai_df = permissions_df[
    [username_column, permission_count_column]
].copy()

ai_df.columns = [
    "username",
    "permission_count"
]

ai_df["permission_count"] = pd.to_numeric(
    ai_df["permission_count"],
    errors="coerce"
)

ai_df = ai_df.dropna(
    subset=[
        "username",
        "permission_count"
    ]
)

ai_df["username"] = ai_df["username"].astype(str)
ai_df["permission_count"] = ai_df["permission_count"].astype(float)


# ================================================================
# LOAD USER ROLE DATA IF AVAILABLE
# ================================================================

role_distribution_file = find_existing_file([
    OUTPUT_DIR / "user_role_distribution.csv",
    OUTPUT_DIR / "findings" / "user_role_distribution.csv"
])

if role_distribution_file is not None:

    print(f"\nLoading user role data from:")
    print(role_distribution_file)

    roles_df = pd.read_csv(role_distribution_file)

    role_username_column = find_column(
        roles_df,
        [
            "username",
            "user_name",
            "user",
            "name"
        ]
    )

    role_count_column = find_column(
        roles_df,
        [
            "role_count",
            "roles",
            "rolecount",
            "count"
        ]
    )

    if role_username_column is not None and role_count_column is not None:

        roles_df = roles_df[
            [role_username_column, role_count_column]
        ].copy()

        roles_df.columns = [
            "username",
            "role_count"
        ]

        roles_df["username"] = roles_df["username"].astype(str)

        roles_df["role_count"] = pd.to_numeric(
            roles_df["role_count"],
            errors="coerce"
        ).fillna(0)

        ai_df = ai_df.merge(
            roles_df,
            on="username",
            how="left"
        )

        print("Role count successfully added to AI analysis.")

    else:

        print(
            "Warning: Role distribution file found, "
            "but required columns could not be identified."
        )

        ai_df["role_count"] = 0

else:

    print(
        "\nUser role distribution file was not found."
    )

    print(
        "AI analysis will continue using permission information."
    )

    ai_df["role_count"] = 0


# ================================================================
# LOAD EXCESSIVE PERMISSION FINDINGS
# ================================================================

excessive_permissions_file = find_existing_file([
    OUTPUT_DIR / "excessive_permissions.csv",
    OUTPUT_DIR / "findings" / "excessive_permissions.csv"
])

ai_df["existing_excessive_finding"] = 0

if excessive_permissions_file is not None:

    print(f"\nLoading existing excessive permission findings from:")
    print(excessive_permissions_file)

    excessive_df = pd.read_csv(excessive_permissions_file)

    excessive_username_column = find_column(
        excessive_df,
        [
            "username",
            "user_name",
            "user",
            "name"
        ]
    )

    if excessive_username_column is not None:

        excessive_users = set(
            excessive_df[
                excessive_username_column
            ].dropna().astype(str)
        )

        ai_df["existing_excessive_finding"] = (
            ai_df["username"].isin(excessive_users).astype(int)
        )

        print(
            f"Existing excessive permission findings identified: "
            f"{len(excessive_users)}"
        )


# ================================================================
# FEATURE ENGINEERING
# ================================================================

print("\n" + "-" * 70)
print("BUILDING AI FEATURES")
print("-" * 70)

# Basic numerical features
ai_df["permission_per_role"] = np.where(
    ai_df["role_count"] > 0,
    ai_df["permission_count"] / ai_df["role_count"],
    ai_df["permission_count"]
)

# Calculate statistical indicators
permission_mean = ai_df["permission_count"].mean()
permission_std = ai_df["permission_count"].std()

if pd.isna(permission_std) or permission_std == 0:
    permission_std = 1

ai_df["permission_z_score"] = (
    ai_df["permission_count"] - permission_mean
) / permission_std

role_mean = ai_df["role_count"].mean()
role_std = ai_df["role_count"].std()

if pd.isna(role_std) or role_std == 0:
    role_std = 1

ai_df["role_z_score"] = (
    ai_df["role_count"] - role_mean
) / role_std


# Select features for machine learning
feature_columns = [
    "permission_count",
    "role_count",
    "permission_per_role",
    "permission_z_score",
    "role_z_score"
]

X = ai_df[feature_columns].copy()

X = X.replace(
    [np.inf, -np.inf],
    np.nan
).fillna(0)


# ================================================================
# FEATURE SCALING
# ================================================================

print("\nScaling AI features...")

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# ================================================================
# AI MODEL 1 - ISOLATION FOREST
# ================================================================

print("\n" + "-" * 70)
print("AI MODEL 1: ISOLATION FOREST ANOMALY DETECTION")
print("-" * 70)

# Isolation Forest requires enough records to analyze
if len(ai_df) >= 10:

    isolation_forest = IsolationForest(
        n_estimators=200,
        contamination=0.10,
        random_state=42
    )

    anomaly_prediction = isolation_forest.fit_predict(
        X_scaled
    )

    anomaly_score = isolation_forest.decision_function(
        X_scaled
    )

    ai_df["anomaly_prediction"] = anomaly_prediction
    ai_df["anomaly_score"] = anomaly_score

    # -1 means anomaly in Isolation Forest
    ai_df["is_anomaly"] = (
        ai_df["anomaly_prediction"] == -1
    ).astype(int)

    # Convert to easier risk score
    ai_df["anomaly_risk_score"] = (
        -ai_df["anomaly_score"]
    )

    print(
        f"Anomalies detected: "
        f"{ai_df['is_anomaly'].sum()}"
    )

else:

    print(
        "Not enough records for Isolation Forest. "
        "At least 10 users are required."
    )

    ai_df["anomaly_prediction"] = 1
    ai_df["anomaly_score"] = 0
    ai_df["is_anomaly"] = 0
    ai_df["anomaly_risk_score"] = 0


# ================================================================
# AI MODEL 2 - K-MEANS CLUSTERING
# ================================================================

print("\n" + "-" * 70)
print("AI MODEL 2: K-MEANS PRIVILEGE PATTERN CLUSTERING")
print("-" * 70)

if len(ai_df) >= 3:

    number_of_clusters = min(4, len(ai_df))

    kmeans = KMeans(
        n_clusters=number_of_clusters,
        random_state=42,
        n_init=20
    )

    ai_df["ai_cluster"] = kmeans.fit_predict(
        X_scaled
    )

    # Calculate average privilege level for each cluster
    cluster_summary = (
        ai_df.groupby("ai_cluster")
        .agg(
            average_permission_count=(
                "permission_count",
                "mean"
            ),
            average_role_count=(
                "role_count",
                "mean"
            ),
            users_in_cluster=(
                "username",
                "count"
            )
        )
        .reset_index()
    )

    # Highest average permission count = highest privilege cluster
    cluster_summary = cluster_summary.sort_values(
        by="average_permission_count",
        ascending=False
    ).reset_index(drop=True)

    cluster_summary["cluster_risk_rank"] = (
        cluster_summary.index + 1
    )

    cluster_summary["cluster_risk_level"] = np.select(
        [
            cluster_summary["cluster_risk_rank"] == 1,
            cluster_summary["cluster_risk_rank"] == 2,
            cluster_summary["cluster_risk_rank"] == 3
        ],
        [
            "Critical",
            "High",
            "Medium"
        ],
        default="Low"
    )

    ai_df = ai_df.merge(
        cluster_summary[
            [
                "ai_cluster",
                "cluster_risk_rank",
                "cluster_risk_level"
            ]
        ],
        on="ai_cluster",
        how="left"
    )

    print(
        f"Users grouped into {number_of_clusters} "
        f"AI privilege clusters."
    )

else:

    ai_df["ai_cluster"] = 0
    ai_df["cluster_risk_rank"] = 1
    ai_df["cluster_risk_level"] = "Medium"


# ================================================================
# COMBINED AI RISK SCORE
# ================================================================

print("\n" + "-" * 70)
print("CALCULATING COMBINED AI RISK ASSESSMENT")
print("-" * 70)

# Normalize permission count to 0-40 points
max_permissions = ai_df["permission_count"].max()

if max_permissions > 0:

    permission_risk = (
        ai_df["permission_count"] / max_permissions
    ) * 40

else:

    permission_risk = 0


# Normalize role count to 0-20 points
max_roles = ai_df["role_count"].max()

if max_roles > 0:

    role_risk = (
        ai_df["role_count"] / max_roles
    ) * 20

else:

    role_risk = 0


# AI anomaly adds 25 points
anomaly_risk = ai_df["is_anomaly"] * 25


# Existing excessive finding adds 15 points
existing_finding_risk = (
    ai_df["existing_excessive_finding"] * 15
)


ai_df["ai_risk_score"] = (
    permission_risk
    + role_risk
    + anomaly_risk
    + existing_finding_risk
)

ai_df["ai_risk_score"] = (
    ai_df["ai_risk_score"]
    .clip(0, 100)
    .round(2)
)


# ================================================================
# ASSIGN FINAL RISK LEVEL
# ================================================================

def determine_risk_level(row):

    score = row["ai_risk_score"]

    if score >= 75:
        return "Critical"

    elif score >= 55:
        return "High"

    elif score >= 30:
        return "Medium"

    return "Low"


ai_df["ai_risk_level"] = ai_df.apply(
    determine_risk_level,
    axis=1
)


# ================================================================
# GENERATE AI EXPLANATIONS
# ================================================================

def generate_ai_explanation(row):

    reasons = []

    # Permission-based explanation
    if row["permission_count"] >= ai_df[
        "permission_count"
    ].quantile(0.90):

        reasons.append(
            "User has a permission count within the highest "
            "10% of the organization"
        )

    elif row["permission_count"] >= ai_df[
        "permission_count"
    ].median():

        reasons.append(
            "User has an above-median number of permissions"
        )

    # Role-based explanation
    if row["role_count"] > 0:

        if row["role_count"] >= ai_df[
            "role_count"
        ].quantile(0.90):

            reasons.append(
                "User holds an unusually high number of roles"
            )

    # Isolation Forest explanation
    if row["is_anomaly"] == 1:

        reasons.append(
            "Isolation Forest detected an unusual access pattern"
        )

    # K-Means explanation
    if row["cluster_risk_level"] in [
        "Critical",
        "High"
    ]:

        reasons.append(
            f"K-Means placed the user in a "
            f"{row['cluster_risk_level'].lower()}-privilege cluster"
        )

    # Existing finding explanation
    if row["existing_excessive_finding"] == 1:

        reasons.append(
            "User was previously identified with potentially "
            "excessive permissions"
        )

    if not reasons:

        reasons.append(
            "User access pattern is currently within the normal "
            "range of the analyzed population"
        )

    return ". ".join(reasons) + "."


ai_df["ai_risk_explanation"] = ai_df.apply(
    generate_ai_explanation,
    axis=1
)


# ================================================================
# ADD AI RECOMMENDATION
# ================================================================

def generate_recommendation(row):

    if row["ai_risk_level"] == "Critical":

        return (
            "Immediate security review recommended. "
            "Validate business need and remove unnecessary "
            "permissions using least-privilege principles."
        )

    elif row["ai_risk_level"] == "High":

        return (
            "Prioritize this account for access review. "
            "Review role assignments and confirm elevated "
            "permissions are justified."
        )

    elif row["ai_risk_level"] == "Medium":

        return (
            "Schedule a standard access review and monitor "
            "future changes to permissions and role assignments."
        )

    return (
        "No immediate remediation required. "
        "Continue periodic access monitoring."
    )


ai_df["ai_recommendation"] = ai_df.apply(
    generate_recommendation,
    axis=1
)


# ================================================================
# SORT FINAL RESULTS
# ================================================================

ai_df = ai_df.sort_values(
    by=[
        "ai_risk_score",
        "permission_count"
    ],
    ascending=[
        False,
        False
    ]
).reset_index(drop=True)


# ================================================================
# SAVE COMPLETE AI RISK ASSESSMENT
# ================================================================

risk_assessment_file = (
    OUTPUT_DIR / "ai_user_risk_assessment.csv"
)

ai_df.to_csv(
    risk_assessment_file,
    index=False
)


# ================================================================
# SAVE AI ANOMALY FINDINGS
# ================================================================

anomaly_findings_df = ai_df[
    ai_df["is_anomaly"] == 1
].copy()

anomaly_findings_file = (
    OUTPUT_DIR / "ai_anomaly_findings.csv"
)

anomaly_findings_df.to_csv(
    anomaly_findings_file,
    index=False
)


# ================================================================
# SAVE AI CLUSTER ANALYSIS
# ================================================================

cluster_output_columns = [
    "username",
    "permission_count",
    "role_count",
    "ai_cluster",
    "cluster_risk_rank",
    "cluster_risk_level",
    "ai_risk_score",
    "ai_risk_level"
]

cluster_output_columns = [
    column
    for column in cluster_output_columns
    if column in ai_df.columns
]

cluster_analysis_df = ai_df[
    cluster_output_columns
].copy()

cluster_analysis_file = (
    OUTPUT_DIR / "ai_cluster_analysis.csv"
)

cluster_analysis_df.to_csv(
    cluster_analysis_file,
    index=False
)


# ================================================================
# DISPLAY SUMMARY
# ================================================================

print("\n" + "=" * 70)
print("AI PRIVILEGE ANALYSIS COMPLETE")
print("=" * 70)

print(
    f"\nTotal users analyzed: {len(ai_df)}"
)

print(
    f"AI anomalies detected: "
    f"{int(ai_df['is_anomaly'].sum())}"
)

print("\nAI Risk Level Distribution:")

risk_distribution = (
    ai_df["ai_risk_level"]
    .value_counts()
)

for risk_level in [
    "Critical",
    "High",
    "Medium",
    "Low"
]:

    count = risk_distribution.get(
        risk_level,
        0
    )

    print(
        f"  {risk_level}: {count}"
    )

print("\nFiles created successfully:")

print(
    f"  1. {risk_assessment_file}"
)

print(
    f"  2. {anomaly_findings_file}"
)

print(
    f"  3. {cluster_analysis_file}"
)

print("\nAI MODELS USED:")

print(
    "  1. Isolation Forest - Anomaly Detection"
)

print(
    "  2. K-Means - Privilege Pattern Clustering"
)

print("\nAnalysis completed successfully.\n")