"""
Stage 03 Diagnostics — Intermediate Artifact Validation
================================================================================
Validates the artifacts produced by Stage 03:
    - quality_summary.json
    - facility_metrics.csv
    - column_profiles.json

Checks performed:
    - file existence
    - JSON validity
    - CSV validity
    - required keys/columns
    - non-empty metrics
    - facility ID consistency with Stage 02 cleaned data
    - column name consistency with Stage 02 cleaned data

Usage:
    python scripts/diagnostics/stage03/check_intermediate_artifacts.py
"""

import json
import logging
from pathlib import Path

import pandas as pd

# ------------------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------------------

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] stage03_diag: %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

# ------------------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------------------

INTERMEDIATE_DIR = Path("data/stage03_intermediate")
SUMMARY_PATH = INTERMEDIATE_DIR / "quality_summary.json"
FACILITY_PATH = INTERMEDIATE_DIR / "facility_metrics.csv"
PROFILES_PATH = INTERMEDIATE_DIR / "column_profiles.json"

# FIXED: Stage 02 cleaned data lives here (not raw POS)
CLEANED_DATA_PATH = Path("data/stage02_cleaned/cleaned_data.csv")


# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------


def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing JSON artifact: {path}")
    with path.open("r") as f:
        return json.load(f)


def load_csv(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing CSV artifact: {path}")
    return pd.read_csv(path)


# ------------------------------------------------------------------------------
# Diagnostics
# ------------------------------------------------------------------------------


def check_quality_summary():
    logger.info("Checking quality_summary.json...")
    summary = load_json(SUMMARY_PATH)

    required_keys = [
        "total_rows",
        "column_count",
        "missingness_summary",
        "quality_score",
    ]

    for key in required_keys:
        if key not in summary:
            raise ValueError(f"Missing key in summary: {key}")

    if summary["total_rows"] <= 0:
        raise ValueError("total_rows must be > 0")

    logger.info("quality_summary.json OK.")


def check_facility_metrics():
    logger.info("Checking facility_metrics.csv...")
    df = load_csv(FACILITY_PATH)

    required_cols = [
        "facility_id",
        "row_count",
        "missingness_rate",
        "quality_score",
    ]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column in facility metrics: {col}")

    if df.empty:
        raise ValueError("facility_metrics.csv is empty")

    logger.info("facility_metrics.csv OK.")


def check_column_profiles():
    logger.info("Checking column_profiles.json...")
    profiles = load_json(PROFILES_PATH)

    if not profiles:
        raise ValueError("column_profiles.json is empty")

    for col, metrics in profiles.items():
        required_keys = [
            "null_count",
            "distinct_count",
            "inferred_dtype",
            "quality_score",
        ]
        for key in required_keys:
            if key not in metrics:
                raise ValueError(f"Missing key '{key}' in column profile for {col}")

    logger.info("column_profiles.json OK.")


def check_consistency_with_cleaned_data():
    logger.info("Checking consistency with cleaned Stage 02 data...")

    df_clean = load_csv(CLEANED_DATA_PATH)
    df_facility = load_csv(FACILITY_PATH)
    profiles = load_json(PROFILES_PATH)

    # Facility ID consistency --------------------------------------------------
    cleaned_facilities = set(df_clean["facility_id"].unique())
    facility_metrics_facilities = set(df_facility["facility_id"].unique())

    if not facility_metrics_facilities.issubset(cleaned_facilities):
        raise ValueError(
            "Facility IDs in facility_metrics.csv do not match cleaned data"
        )

    # Column name consistency --------------------------------------------------
    cleaned_columns = set(df_clean.columns)
    profile_columns = set(profiles.keys())

    if not profile_columns.issubset(cleaned_columns):
        raise ValueError("Column profiles contain columns not present in cleaned data")

    logger.info("Consistency checks OK.")


# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------


def main():
    logger.info("Starting Stage 03 intermediate artifact diagnostics...")

    check_quality_summary()
    check_facility_metrics()
    check_column_profiles()
    check_consistency_with_cleaned_data()

    logger.info("Stage 03 diagnostics completed successfully.")


if __name__ == "__main__":
    main()
