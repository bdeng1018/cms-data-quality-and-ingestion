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
    - Deterministic logging for reproducibility
    - Clear separation between loading, computing, and writing
    - Minimal assumptions about upstream stages
"""

import json
import logging
from pathlib import Path

import pandas as pd

from src.stage03_data_quality.quality_engine import run_stage03_quality
from src.stage03_data_quality.quality_writer import (
    write_column_profiles,
    write_facility_metrics,
    write_quality_summary,
)
from utils.file_io import ensure_directory

# ==============================================================================
# Module‑level logger placeholder (reconfigured deterministically in main)
# ==============================================================================
logger = logging.getLogger("stage03_runner")


# ==============================================================================
# Deterministic Logging Configuration
# ==============================================================================
def configure_logging(log_path: Path) -> logging.Logger:
    """
    Configure deterministic logging for Stage 03 runner.
    Ensures:
        - Log file is always created
        - Handlers are cleared each run
        - No timestamps (deterministic)
        - UTF-8 encoding
        - Overwrite mode
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("stage03_runner")
    logger.setLevel(logging.INFO)

    # Deterministic: clear handlers each run
    logger.handlers.clear()

    handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    formatter = logging.Formatter("%(message)s")  # deterministic, no timestamps
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


# ==============================================================================
# File locations
# ==============================================================================
SCHEMA_PATH = Path("data/stage01_schema/schema.json")
CLEANED_DATA_PATH = Path("data/stage02_cleaned/cleaned_data.csv")
OUTPUT_DIR = Path("data/stage03_intermediate")
LOG_PATH = OUTPUT_DIR / "quality.log"  # ✔ your chosen filename


# ==============================================================================
# Loader helpers
# ==============================================================================
def load_schema(logger) -> dict:
    logger.info(f"Loading schema → {SCHEMA_PATH}")

    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_PATH}")

    with SCHEMA_PATH.open("r") as f:
        schema = json.load(f)

    logger.info("Schema loaded successfully.")
    return schema


def load_cleaned_data(logger) -> pd.DataFrame:
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
    logger = configure_logging(LOG_PATH)
    logger.info("STAGE03_LOG_VERSION=1")
    logger.info("Starting Stage 03 runner...")

    schema = load_schema(logger)
    df = load_cleaned_data(logger)

    logger.info("Executing Stage 03 quality engine...")
    summary_dict, df_facility, column_profiles = run_stage03_quality(df, schema)

    logger.info("Ensuring Stage 03 output directory exists...")
    ensure_directory(str(OUTPUT_DIR))

    logger.info("Writing Stage 03 intermediate artifacts...")

    write_quality_summary(summary_dict, base_dir=OUTPUT_DIR)
    write_facility_metrics(df_facility, base_dir=OUTPUT_DIR)
    write_column_profiles(column_profiles, base_dir=OUTPUT_DIR)

    logger.info("Stage 03 runner completed successfully.")
    logger.info(f"Intermediate artifacts written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
