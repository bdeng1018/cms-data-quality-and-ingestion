"""
check_ingestion.py
Stage 02 — Diagnostics for Raw Ingestion & Cleaning
================================================================================
This diagnostic utility verifies:

1. Raw POS/QIES ingestion:
   - File existence
   - Minimal structure
   - Column presence
   - Load success

2. Stage 02 cleaning output:
   - cleaned_data.csv existence
   - Schema alignment
   - Column completeness
   - Basic dtype checks
   - Row-count sanity

This script is intended for Branch 1 smoke testing.
"""

import argparse
import os

import pandas as pd

from src.stage01_schema_definition.schema_loader import load_schema
from stage02_raw_ingestion.pos_ingestion import PosIngestionSource
from stage02_raw_ingestion.qies_ingestion import QiesIngestionSource
from utils.logging_utils import get_logger


# ==============================================================================
# Raw POS diagnostics
# ==============================================================================
def diagnose_pos(path: str) -> None:
    logger = get_logger("diagnostics_pos")
    logger.info(f"Diagnosing POS ingestion for file: {path}")

    src = PosIngestionSource(path)
    df = src.load_raw()
    src.validate_minimal_structure(df)

    print("\n=== POS INGESTION DIAGNOSTICS ===")
    print(f"File: {path}")
    print(f"Shape: {df.shape}")
    print(f"Columns ({len(df.columns)}): {list(df.columns)}")
    print("Status: PASS\n")


# ==============================================================================
# Raw QIES diagnostics
# ==============================================================================
def diagnose_qies(path: str) -> None:
    logger = get_logger("diagnostics_qies")
    logger.info(f"Diagnosing QIES ingestion for file: {path}")

    src = QiesIngestionSource(path)
    df = src.load_raw()
    src.validate_minimal_structure(df)

    print("\n=== QIES INGESTION DIAGNOSTICS ===")
    print(f"File: {path}")
    print(f"Shape: {df.shape}")
    print(f"Columns ({len(df.columns)}): {list(df.columns)}")
    print("Status: PASS\n")


# ==============================================================================
# Stage 02 cleaned-data diagnostics
# ==============================================================================
def diagnose_cleaned(path: str) -> None:
    logger = get_logger("diagnostics_cleaned")
    logger.info(f"Diagnosing Stage 02 cleaned output: {path}")

    if not os.path.exists(path):
        print("\n=== CLEANED DATA DIAGNOSTICS ===")
        print(f"File missing: {path}")
        print("Status: FAIL — cleaned_data.csv not found\n")
        return

    df = pd.read_csv(path)
    schema = load_schema()
    schema_cols = [f["name"] for f in schema["fields"]]

    missing_cols = [c for c in schema_cols if c not in df.columns]
    extra_cols = [c for c in df.columns if c not in schema_cols]

    print("\n=== CLEANED DATA DIAGNOSTICS ===")
    print(f"File: {path}")
    print(f"Shape: {df.shape}")

    # Column completeness ------------------------------------------------------
    print(f"\nSchema columns: {len(schema_cols)}")
    print(f"Missing columns: {missing_cols}")
    print(f"Extra columns: {extra_cols}")

    # Row-count sanity ---------------------------------------------------------
    if df.shape[0] == 0:
        print("Row-count check: FAIL — cleaned dataset is empty")
    else:
        print("Row-count check: PASS")

    # Facility ID check --------------------------------------------------------
    if "facility_id" in df.columns:
        null_facility = df["facility_id"].isna().sum()
        print(f"Null facility_id count: {null_facility}")
    else:
        print("facility_id missing from cleaned dataset")

    # Basic dtype checks -------------------------------------------------------
    print("\nDtype checks:")
    for field in schema["fields"]:
        col = field["name"]
        expected = field["type"]
        if col in df.columns:
            actual = str(df[col].dtype)
            print(f"  {col}: expected={expected}, actual={actual}")

    print("\nStatus: PASS (if no FAIL messages above)\n")


# ==============================================================================
# Entrypoint
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Stage 02 diagnostics for POS/QIES ingestion and cleaned output."
    )
    parser.add_argument(
        "mode", choices=["pos", "qies", "cleaned"], help="Which diagnostic to run."
    )
    parser.add_argument("path", help="Path to input file (raw or cleaned).")

    args = parser.parse_args()

    if args.mode == "pos":
        diagnose_pos(args.path)
    elif args.mode == "qies":
        diagnose_qies(args.path)
    else:
        diagnose_cleaned(args.path)


if __name__ == "__main__":
    main()
