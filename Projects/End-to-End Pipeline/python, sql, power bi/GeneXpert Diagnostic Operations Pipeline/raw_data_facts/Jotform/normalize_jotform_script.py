import pandas as pd
import re

# -------------------------
# CONFIG
# -------------------------
INPUT_FILE = "service_jotform.xlsx"
OUTPUT_FILE = "fact_service_normalized.csv"

SERVICE_COL = "TYPE OF SERVICE"

# Canonical service labels (final output)
CANONICAL_SERVICES = {
    "INSTALLATION": ["INSTALLATION"],
    "REPAIR": ["REPAIR"],
    "CALIBRATION": ["CALIBRATION"],
    "MAINTENANCE": ["MAINTENANCE"],
    "TROUBLESHOOTING": ["TROUBLESHOOT"],
    "ON-SITE ASSISTANCE": [
        "ON-SITE ASSISTANCE",
        "ON SITE ASSISTANCE",
        "ON SITE ASSITANCE",   # common typo
        "ONSITE ASSISTANCE"
    ],
}

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_excel(INPUT_FILE, engine="openpyxl")

# -------------------------
# NORMALIZATION FUNCTION
# -------------------------
def classify_services(cell_value):
    """
    One line / token = one claimed service
    Returns a list of canonical service types
    """

    if pd.isna(cell_value):
        return ["OTHERS"]

    text = str(cell_value).upper().strip()

    # Split into atomic claims
    parts = re.split(r"[\n,;/]+", text)
    parts = [p.strip() for p in parts if p.strip()]

    results = []

    for part in parts:
        classified = False

        for canonical, patterns in CANONICAL_SERVICES.items():
            if any(pattern in part for pattern in patterns):
                results.append(canonical)
                classified = True
                break

        # No official service matched → OTHERS
        if not classified:
            results.append("OTHERS")

    return results

# -------------------------
# APPLY & EXPLODE
# -------------------------
df["service_type"] = df[SERVICE_COL].apply(classify_services)
df_long = df.explode("service_type", ignore_index=True)

# -------------------------
# OUTPUT
# -------------------------
df_long.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print(f"Created {OUTPUT_FILE} with {len(df_long)} rows.")