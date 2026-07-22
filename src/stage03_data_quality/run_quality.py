"""
Stage 03 Runner
================================================================================
Official entrypoint for Stage 03 of the CMS POS/QIES ingestion pipeline.

Responsibilities:
    1. Load Stage 01 schema metadata
    2. Load Stage 02 cleaned data
    3. Execute Stage 03 quality engine
    4. Persist intermediate artifacts into data/stage03_intermediate/

Design principles:
    - Strong logging for pipeline observability
    - Clear separation between loading, computing, and writing
    - Minimal assumptions about upstream stages
"""

import json
import logging
from pathlib import Path

import pandas as pd

from utils.file_io import ensure_directory

from .quality_engine import run_stage03_quality
from .quality_writer import (
    write_column_profiles,
    write_facility_metrics,
    write_quality_summary,
)

# ==============================================================================
# Logging configuration
# ==============================================================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] stage03_runner: %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)


# ==============================================================================
# File locations
# ==============================================================================
SCHEMA_PATH = Path("data/stage01_schema/schema.json")
CLEANED_DATA_PATH = Path("data/stage02_cleaned/cleaned_data.csv")
OUTPUT_DIR = Path("data/stage03_intermediate")


# ==============================================================================
# Loader helpers
# ==============================================================================
def load_schema() -> dict:
    logger.info(f"Loading schema → {SCHEMA_PATH}")

    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_PATH}")

    with SCHEMA_PATH.open("r") as f:
        schema = json.load(f)

    logger.info("Schema loaded successfully.")
    return schema


def load_cleaned_data() -> pd.DataFrame:
    logger.info(f"Loading cleaned data → {CLEANED_DATA_PATH}")

    if not CLEANED_DATA_PATH.exists():
        raise FileNotFoundError(f"Cleaned data file not found: {CLEANED_DATA_PATH}")

    df = pd.read_csv(CLEANED_DATA_PATH)
    logger.info(
        f"Cleaned data loaded successfully. Rows={len(df)}, Columns={len(df.columns)}"
    )
    return df


# ==============================================================================
# Main runner
# ==============================================================================
def main() -> None:
    logger.info("Starting Stage 03 runner...")

    schema = load_schema()
    df = load_cleaned_data()

    logger.info("Executing Stage 03 quality engine...")
    summary_dict, df_facility, column_profiles = run_stage03_quality(df, schema)

    logger.info("Ensuring Stage 03 output directory exists...")
    ensure_directory(str(OUTPUT_DIR))

    logger.info("Writing Stage 03 intermediate artifacts...")

    # ⭐ Pass OUTPUT_DIR explicitly — prevents pytest from corrupting pipeline artifacts
    write_quality_summary(summary_dict, base_dir=OUTPUT_DIR)
    write_facility_metrics(df_facility, base_dir=OUTPUT_DIR)
    write_column_profiles(column_profiles, base_dir=OUTPUT_DIR)

    logger.info("Stage 03 runner completed successfully.")
    logger.info(f"Intermediate artifacts written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
