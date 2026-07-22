"""
run_ingestion.py
Stage 02 — Local Ingestion Runner Stub

Provides a simple manual entry point for testing POS/QIES ingestion
without requiring the full pipeline runner (Stage 05). Useful for
development, diagnostics, and Branch 1 smoke testing.
"""

import sys

import pandas as pd

from utils.logging_utils import get_logger

from .pos_ingestion import PosIngestionSource
from .qies_ingestion import QiesIngestionSource


def run_pos_ingestion(path: str) -> pd.DataFrame:
    """
    Returns
    -------
    pd.DataFrame
        Loaded and minimally validated raw dataset.
    """
    logger = get_logger("run_ingestion")
    logger.info(f"Running POS ingestion for file: {path}")

    pos = PosIngestionSource(path)
    df = pos.load_raw()
    pos.validate_minimal_structure(df)

    logger.info(f"POS ingestion complete. Shape: {df.shape}")
    return df


def run_qies_ingestion(path: str) -> pd.DataFrame:
    """
    Returns
    -------
    pd.DataFrame
        Loaded and minimally validated raw dataset.
    """
    logger = get_logger("run_ingestion")
    logger.info(f"Running QIES ingestion for file: {path}")

    qies = QiesIngestionSource(path)
    df = qies.load_raw()
    qies.validate_minimal_structure(df)

    logger.info(f"QIES ingestion complete. Shape: {df.shape}")
    return df


if __name__ == "__main__":
    """
    Example usage:
        python run_ingestion.py pos /path/to/pos.csv
        python run_ingestion.py qies /path/to/qies.csv
    """

    if len(sys.argv) != 3:
        print("Usage: python run_ingestion.py [pos|qies] <raw_file_path>")
        sys.exit(1)

    source_type = sys.argv[1].lower()
    raw_path = sys.argv[2]

    if source_type == "pos":
        run_pos_ingestion(raw_path)
    elif source_type == "qies":
        run_qies_ingestion(raw_path)
    else:
        print("Invalid source type. Use 'pos' or 'qies'.")
        sys.exit(1)
