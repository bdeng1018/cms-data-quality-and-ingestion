"""
constants.py
Stage 02 — Raw Ingestion Minimal Column Requirements

Defines the essential columns required for POS and QIES ingestion.
These are NOT full schemas (Stage 01 handles that). Instead, these
represent the minimal shape guarantees that Stage 02 enforces.

Branch 1 only requires lightweight column presence checks.
"""

# Minimal required columns for CMS POS raw ingestion
POS_MIN_COLUMNS = [
    "ccn",
    "provider_type",
    "address",
    "city",
    "state",
    "zip",
    "ownership",
]

# Minimal required columns for CMS QIES raw ingestion
QIES_MIN_COLUMNS = ["ccn", "qm_rating", "qm_score", "participation_flag"]
