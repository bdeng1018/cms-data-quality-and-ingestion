"""
check_ingestion.py
Stage 02 — Diagnostics for Raw Ingestion

Provides a simple diagnostic utility to verify that POS/QIES ingestion
modules can load raw files, validate minimal structure, and log results.

This script is intended for Branch 1 smoke testing.
"""

import argparse

from stage02_raw_ingestion.pos_ingestion import PosIngestionSource
from stage02_raw_ingestion.qies_ingestion import QiesIngestionSource
from utils.logging_utils import get_logger


def diagnose_pos(path: str) -> None:
    logger = get_logger("diagnostics_pos")
    logger.info(f"Diagnosing POS ingestion for file: {path}")

    src = PosIngestionSource(path)
    df = src.load_raw()
    src.validate_minimal_structure(df)

    print("\n=== POS INGESTION DIAGNOSTICS ===")
    print(f"File: {path}")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("Status: PASS\n")


def diagnose_qies(path: str) -> None:
    logger = get_logger("diagnostics_qies")
    logger.info(f"Diagnosing QIES ingestion for file: {path}")

    src = QiesIngestionSource(path)
    df = src.load_raw()
    src.validate_minimal_structure(df)

    print("\n=== QIES INGESTION DIAGNOSTICS ===")
    print(f"File: {path}")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("Status: PASS\n")


def main():
    parser = argparse.ArgumentParser(
        description="Stage 02 ingestion diagnostics for POS/QIES."
    )
    parser.add_argument(
        "source", choices=["pos", "qies"], help="Which ingestion source to diagnose."
    )
    parser.add_argument("path", help="Path to raw input file.")

    args = parser.parse_args()

    if args.source == "pos":
        diagnose_pos(args.path)
    else:
        diagnose_qies(args.path)


if __name__ == "__main__":
    main()
