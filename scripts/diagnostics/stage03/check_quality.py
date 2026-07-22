"""
Stage 03 Diagnostics — Quality Checks
================================================================================
This script provides a CLI entry point for running Stage 03 quality diagnostics
on the Stage 02 cleaned dataset.

It loads:
    - Stage 01 schema.json
    - Stage 02 cleaned_data.csv

Then it runs:
    - Stage 03 quality engine (pure computation)

Finally it prints:
    - dataset-level metrics
    - facility-level metrics
    - column-level profiles

Usage:
    python check_quality.py --file data/stage02_cleaned/cleaned_data.csv
"""

import argparse
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd

from src.stage01_schema_definition.schema_loader import load_schema
from src.stage03_data_quality.quality_engine import run_stage03_quality


def to_python_scalar(value):
    """Convert numpy scalar types to native Python types."""
    if isinstance(value, np.generic):
        return value.item()
    return value


def sanitize_dict(d: dict) -> dict:
    """Recursively sanitize dictionaries containing NumPy scalar values."""
    clean = {}
    for k, v in d.items():
        if isinstance(v, dict):
            clean[k] = sanitize_dict(v)
        else:
            clean[k] = to_python_scalar(v)
    return clean


# ------------------------------------------------------------------------------
# Logging configuration
# ------------------------------------------------------------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

LOG_PATH = Path("logs/quality.log")
handler = logging.FileHandler(LOG_PATH)
formatter = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# ------------------------------------------------------------------------------
# Loader helpers
# ------------------------------------------------------------------------------
def load_cleaned(path: Path) -> pd.DataFrame:
    """
    Load Stage 02 cleaned dataset.
    """
    if not path.exists():
        logger.error(f"Cleaned dataset not found: {path}")
        raise FileNotFoundError(f"Cleaned dataset not found: {path}")

    logger.info(f"Loading cleaned dataset: {path}")
    df = pd.read_csv(path)
    logger.info(f"Loaded cleaned dataset with shape: {df.shape}")
    return df


# ------------------------------------------------------------------------------
# CLI Entrypoint
# ------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Run Stage 03 Quality Diagnostics")
    parser.add_argument(
        "--file",
        required=True,
        help="Path to cleaned_data.csv (Stage 02 output)",
    )

    parser.add_argument(
        "--type",
        required=False,
        choices=["pos", "qies", "combined"],
        help="Specify dataset type for diagnostics.",
    )

    args = parser.parse_args()

    # dataset_type = args.type or "pos"   # default if omitted
    cleaned_path = Path(args.file)

    # Load Stage 01 schema
    logger.info("Loading Stage 01 schema...")
    schema = load_schema()

    # Load Stage 02 cleaned dataset
    try:
        df = load_cleaned(cleaned_path)
    except Exception as e:
        logger.error(f"Failed to load cleaned dataset: {e}")
        return

    # Run Stage 03 quality engine
    logger.info("Running Stage 03 quality engine...")
    summary_dict, df_facility, column_profiles = run_stage03_quality(df, schema)

    # Print dataset-level metrics
    print("\n=== Stage 03 Dataset-Level Metrics ===")
    for k, v in summary_dict.items():
        print(f"{k}: {v}")

    # Print facility-level metrics
    print("\n=== Stage 03 Facility-Level Metrics ===")
    print(df_facility.to_string(index=False))

    # Print column-level profiles (summaries only)
    print("\n=== Stage 03 Column-Level Profiles (Summary) ===")
    for col, profile in column_profiles.items():
        print(
            f"{col}: nulls={profile['null_count']}, distinct={profile['distinct_count']}"
        )

    print("\nDiagnostics complete.\n")

    # Log summary
    logger.info("Dataset-level metrics:")
    clean_summary = sanitize_dict(summary_dict)
    logger.info(json.dumps(clean_summary, indent=2))

    logger.info("Facility-level metrics:")
    logger.info(df_facility.to_string(index=False))

    logger.info("Column-level profiles:")
    clean_profiles = sanitize_dict(column_profiles)
    logger.info(json.dumps(clean_profiles, indent=2))

    logger.info("Stage 03 diagnostics complete.")


if __name__ == "__main__":
    main()
