"""
Stage 03 Diagnostics — Quality Checks

This script provides a CLI entry point for running Stage 03 quality checks
on raw POS/QIES data loaded from Stage 02.

It loads a CSV/Parquet file, runs the quality engine, prints a summary,
and writes results to logs/quality.log.

Usage:
    python check_quality.py --file data/stage02_raw/pos_q2_2026.csv --type pos
"""

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

# Import Stage 03 engine
from stage03_data_quality import run_quality_checks

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Log file path
LOG_PATH = Path("logs/quality.log")
handler = logging.FileHandler(LOG_PATH)
formatter = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# Minimal expected columns for POS/QIES
POS_COLUMNS = [
    "ccn",
    "provider_type",
    "address",
    "city",
    "state",
    "zip",
    "ownership",
]

QIES_COLUMNS = [
    "ccn",
    "qm_rating",
    "qm_score",
    "participation_flag",
]


def load_file(path: Path) -> pd.DataFrame:
    """
    Load a raw CSV or Parquet file.

    Args:
        path: Path to the raw file.

    Returns:
        Loaded DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If file extension is unsupported.
    """
    if not path.exists():
        logger.error(f"File not found: {path}")
        raise FileNotFoundError(f"Raw file not found: {path}")

    logger.info(f"Loading raw file: {path}")

    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    elif path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")


def main():
    """
    CLI entry point for Stage 03 diagnostics.

    Steps:
        1. Parse arguments
        2. Load raw file
        3. Select expected columns + key
        4. Run quality checks
        5. Print summary
        6. Log results
    """
    parser = argparse.ArgumentParser(description="Run Stage 03 Quality Checks")
    parser.add_argument("--file", required=True, help="Path to raw POS/QIES file")
    parser.add_argument(
        "--type",
        required=True,
        choices=["pos", "qies"],
        help="Dataset type: pos or qies",
    )

    args = parser.parse_args()
    file_path = Path(args.file)

    try:
        df = load_file(file_path)
    except Exception as e:
        logger.error(f"Failed to load file: {e}")
        sys.exit(1)

    # Select expected columns + key
    if args.type == "pos":
        expected_cols = POS_COLUMNS
        key = "ccn"
    else:
        expected_cols = QIES_COLUMNS
        key = "ccn"

    logger.info(f"Running quality checks for dataset type: {args.type}")

    report = run_quality_checks(df, expected_cols, key)

    # Print summary to console
    print("\n=== Stage 03 Quality Report ===")
    print(f"Rows: {report.row_count}")
    print(f"Null Counts: {report.null_counts}")
    print(f"Duplicate Counts: {report.duplicate_counts}")
    print(f"Drift Indicators: {report.drift_indicators}")
    print(f"Warnings: {report.warnings}")
    print("================================\n")

    # Log summary
    logger.info(f"Row count: {report.row_count}")
    logger.info(f"Null counts: {report.null_counts}")
    logger.info(f"Duplicate counts: {report.duplicate_counts}")
    logger.info(f"Drift indicators: {report.drift_indicators}")
    logger.info(f"Warnings: {report.warnings}")

    logger.info("Stage 03 diagnostics complete.")


if __name__ == "__main__":
    main()
