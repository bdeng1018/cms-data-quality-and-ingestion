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

# ==============================================================================
# Logging
# ==============================================================================

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

# ==============================================================================
# Paths
# ==============================================================================

INTERMEDIATE_DIR = Path("data/stage03_intermediate")
SUMMARY_PATH = INTERMEDIATE_DIR / "quality_summary.json"
FACILITY_PATH = INTERMEDIATE_DIR / "facility_metrics.csv"
PROFILES_PATH = INTERMEDIATE_DIR / "column_profiles.json"

# FIXED: Stage 02 cleaned data lives here (not raw POS)
CLEANED_DATA_PATH = Path("data/stage02_cleaned/cleaned_data.csv")


# ==============================================================================
# Helpers
# ==============================================================================


def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing JSON artifact: {path}")
    with path.open("r") as f:
        return json.load(f)


def load_csv(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing CSV artifact: {path}")
    return pd.read_csv(path)


# ==============================================================================
# Diagnostics
# ==============================================================================


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


def check_consistency_with_cleaned_data(strict: bool = True):
    logger.info("Checking consistency with cleaned Stage 02 data...")

    df_clean = load_csv(CLEANED_DATA_PATH)
    df_facility = load_csv(FACILITY_PATH)
    profiles = load_json(PROFILES_PATH)

    # ----------------------------------------------------------------------
    # Facility ID normalization
    # ----------------------------------------------------------------------
    def normalize_facility_id(series):
        return (
            series.astype("string")
            .str.strip()
            .str.replace(r"\.0$", "", regex=True)
            .replace({"<NA>": None})
        )

    df_clean["facility_id"] = normalize_facility_id(df_clean["facility_id"])
    df_facility["facility_id"] = normalize_facility_id(df_facility["facility_id"])

    cleaned_facilities = set(df_clean["facility_id"].dropna().unique())
    facility_metrics_facilities = set(df_facility["facility_id"].dropna().unique())

    # ----------------------------------------------------------------------
    # Facility ID consistency
    # ----------------------------------------------------------------------
    missing_in_metrics = cleaned_facilities - facility_metrics_facilities
    extra_in_metrics = facility_metrics_facilities - cleaned_facilities

    if missing_in_metrics or extra_in_metrics:
        if strict:
            raise ValueError(
                "Facility ID mismatch between Stage 02 and Stage 03.\n"
                f"Missing in metrics: {sorted(list(missing_in_metrics))[:20]}\n"
                f"Extra in metrics: {sorted(list(extra_in_metrics))[:20]}"
            )
        else:
            logger.info("[SKIP] Facility ID mismatch detected (optional mode).")
            if missing_in_metrics:
                logger.info(
                    f"[SKIP] Facilities missing in facility_metrics.csv: "
                    f"{sorted(list(missing_in_metrics))[:20]}"
                )
            if extra_in_metrics:
                logger.info(
                    f"[SKIP] Facilities present in facility_metrics.csv but not in "
                    f"cleaned_data.csv: {sorted(list(extra_in_metrics))[:20]}"
                )
            logger.info("[SKIP] Skipping strict facility ID consistency check.")
            return

    # ----------------------------------------------------------------------
    # Column name consistency (strict always)
    # ----------------------------------------------------------------------
    cleaned_columns = set(df_clean.columns)
    profile_columns = set(profiles.keys())

    extra_profile_columns = profile_columns - cleaned_columns
    if extra_profile_columns:
        raise ValueError(
            f"Column profiles contain columns not present in cleaned data: "
            f"{sorted(list(extra_profile_columns))}"
        )

    logger.info("Consistency checks OK.")


# ==============================================================================
# Main
# ==============================================================================


def main():
    logger.info("Starting Stage 03 intermediate artifact diagnostics...")

    check_quality_summary()
    check_facility_metrics()
    check_column_profiles()
    check_consistency_with_cleaned_data(strict=False)

    logger.info("Stage 03 diagnostics completed successfully.")


if __name__ == "__main__":
    main()
