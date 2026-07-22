"""
constants.py
Stage 02 — Raw Ingestion Minimal Column Requirements

Defines the essential columns required for POS and QIES ingestion.
These are NOT full schemas (Stage 01 handles that). Instead, these
represent the minimal shape guarantees that Stage 02 enforces.

Branch 1 only requires lightweight column presence checks.
"""

# Minimal required columns for CMS POS raw ingestion (raw API fields)
POS_MIN_COLUMNS = [
    "PRVDR_NUM",
    "PRVDR_CTGRY_CD",
    "CITY_NAME",
    "STATE_CD",
    "ZIP_CD",
    "GNRL_CNTL_TYPE_CD",
]

# Minimal required columns for CMS QIES raw ingestion (raw API fields)
QIES_MIN_COLUMNS = [
    "PRVDR_NUM",
    "QM_RATING",
    "QM_SCORE",
    "PRTCPNT_FLAG",
]
