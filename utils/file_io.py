"""
utils/file_io.py
================================================================================
Shared file I/O utilities for the CMS POS/QIES ingestion pipeline.

Originally introduced in Stage 02 (raw ingestion), this module now supports
Stages 01–04 with safe, minimal, and deterministic helpers:

    - Existence checks
    - Directory creation
    - CSV / Parquet readers
    - DataFrame writers
    - Logging for pipeline observability

Design principles:
    - No domain logic
    - No cleaning or validation
    - No mutation of caller-owned objects
    - Safe for all pipeline stages (01–04)
"""

import logging
from pathlib import Path

import pandas as pd

# ==============================================================================
# Logging configuration
# ==============================================================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("[%(levelname)s] utils.file_io: %(message)s")
    )
    logger.addHandler(handler)


# ==============================================================================
# Existence checks
# ==============================================================================
def ensure_exists(path: str | Path) -> None:
    """
    Ensure a file exists before ingestion or reading.

    Parameters
    ----------
    path : str or Path
        File path to validate.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    """
    path = Path(path)
    if not path.exists():
        logger.error(f"File not found: {path}")
        raise FileNotFoundError(f"File not found: {path}")

    logger.info(f"Verified file exists: {path}")


# ==============================================================================
# Directory utilities
# ==============================================================================
def ensure_directory(path: str | Path) -> None:
    """
    Ensure a directory exists. If missing, create it.

    Parameters
    ----------
    path : str or Path
        Directory path to create if missing.

    Notes
    -----
    - Idempotent
    - Safe for Stage 02 landing-zone writes
    - Used by Stage 04 report writer
    """
    if not path:
        return

    path = Path(path)

    if not path.exists():
        logger.info(f"Creating directory: {path}")
        path.mkdir(parents=True, exist_ok=True)
    else:
        logger.info(f"Directory exists: {path}")


# ==============================================================================
# CSV / Parquet readers
# ==============================================================================
def read_csv(path: str | Path) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame.

    Parameters
    ----------
    path : str or Path

    Returns
    -------
    pd.DataFrame
    """
    ensure_exists(path)
    logger.info(f"Reading CSV: {path}")
    return pd.read_csv(path)


def read_parquet(path: str | Path) -> pd.DataFrame:
    """
    Load a Parquet file into a DataFrame.

    Parameters
    ----------
    path : str or Path

    Returns
    -------
    pd.DataFrame
    """
    ensure_exists(path)
    logger.info(f"Reading Parquet: {path}")
    return pd.read_parquet(path)


# ==============================================================================
# DataFrame writer
# ==============================================================================
def write_df(df: pd.DataFrame, path: str | Path) -> None:
    """
    Write a DataFrame to disk (CSV).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to write.
    path : str or Path
        Output CSV path.

    Notes
    -----
    - Used sparingly in Stage 02 landing-zone writes
    - Safe for Stage 04 CSV outputs
    """
    path = Path(path)
    ensure_directory(path.parent)

    logger.info(f"Writing DataFrame → {path}")
    df.to_csv(path, index=False)
