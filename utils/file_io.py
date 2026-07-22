"""
file_io.py
Stage 02 — Raw Ingestion Utilities

Lightweight file I/O helpers used by POS/QIES ingestion modules.
Branch 1 only requires minimal functionality: existence checks,
CSV/Parquet loading, and simple DataFrame returns.

No cleaning, validation, or domain logic belongs here.
"""

import os

import pandas as pd


def ensure_exists(path: str) -> None:
    """
    Ensure the raw file exists before ingestion.
    Raises FileNotFoundError if missing.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Raw file not found: {path}")


def read_csv(path: str) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame.
    Stage 02 only guarantees successful load + DataFrame shape.
    """
    ensure_exists(path)
    return pd.read_csv(path)


def read_parquet(path: str) -> pd.DataFrame:
    """
    Load a Parquet file into a DataFrame.
    """
    ensure_exists(path)
    return pd.read_parquet(path)


def write_df(df: pd.DataFrame, path: str) -> None:
    """
    Write a DataFrame to disk.
    Stage 02 uses this sparingly (landing zone writes).
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
