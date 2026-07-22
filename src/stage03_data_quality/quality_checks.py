"""
Stage 03 — Data Quality Checks (Branch 1 MVP)

This module computes baseline quality metrics for raw POS/QIES data.
It does NOT perform cleaning, normalization, CCN validation, or alignment.
It only profiles the raw DataFrame and returns structured metrics.

Outputs:
    - row count
    - null counts
    - duplicate counts
    - drift indicators
    - warnings list

This module is intentionally lightweight for Branch 1.
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List

import pandas as pd

# Configure module-level logger
logger = logging.getLogger(__name__)


@dataclass
class QualityReport:
    """
    Structured output for Stage 03 quality checks.

    Attributes:
        row_count: Total number of rows in the DataFrame.
        null_counts: Per-column null counts.
        duplicate_counts: Number of duplicate rows based on key fields.
        drift_indicators: Flags for missing or unexpected columns.
        warnings: Human-readable warnings for downstream diagnostics.
    """

    row_count: int
    null_counts: Dict[str, int]
    duplicate_counts: Dict[str, int]
    drift_indicators: Dict[str, List[str]]
    warnings: List[str] = field(default_factory=list)


def compute_null_counts(df: pd.DataFrame) -> Dict[str, int]:
    """
    Compute per-column null counts.

    Args:
        df: Raw POS/QIES DataFrame.

    Returns:
        Dictionary mapping column name → null count.
    """
    logger.debug("Computing null counts.")
    return {str(col): int(nulls) for col, nulls in df.isna().sum().items()}


def compute_duplicate_counts(df: pd.DataFrame, key: str) -> Dict[str, int]:
    """
    Compute duplicate counts based on a key column (e.g., CCN).

    Args:
        df: Raw DataFrame.
        key: Column name used to detect duplicates.

    Returns:
        Dictionary with duplicate count for the key.
    """
    logger.debug(f"Computing duplicate counts using key: {key}")
    if key not in df.columns:
        logger.warning(f"Duplicate check skipped — key '{key}' missing.")
        return {key: 0}

    dup_count = df.duplicated(subset=[key]).sum()
    return {key: int(dup_count)}


def compute_drift(
    df: pd.DataFrame, expected_columns: List[str]
) -> Dict[str, List[str]]:
    """
    Detect schema drift: missing or unexpected columns.

    Args:
        df: Raw DataFrame.
        expected_columns: Columns expected for POS or QIES ingestion.

    Returns:
        Dictionary with lists of missing and unexpected columns.
    """
    logger.debug("Checking for schema drift.")

    actual = set(df.columns)
    expected = set(expected_columns)

    missing = list(expected - actual)
    unexpected = list(actual - expected)

    return {
        "missing_columns": missing,
        "unexpected_columns": unexpected,
    }


def run_quality_checks(
    df: pd.DataFrame, expected_columns: List[str], key: str
) -> QualityReport:
    """
    Run all Stage 03 quality checks on a raw DataFrame.

    Args:
        df: Raw POS/QIES DataFrame.
        expected_columns: Minimal required columns for the dataset.
        key: Column used for duplicate detection (e.g., 'ccn').

    Returns:
        QualityReport containing structured quality metrics.
    """
    logger.info("Running Stage 03 quality checks.")

    row_count = len(df)
    null_counts = compute_null_counts(df)
    duplicate_counts = compute_duplicate_counts(df, key)
    drift_indicators = compute_drift(df, expected_columns)

    warnings = []

    # Add warnings for high-null columns
    for col, nulls in null_counts.items():
        if row_count > 0 and nulls / row_count > 0.5:
            warnings.append(f"High null percentage in column '{col}'.")

    # Add warnings for duplicates
    if duplicate_counts.get(key, 0) > 0:
        warnings.append(f"Duplicate values detected in key column '{key}'.")

    # Add warnings for drift
    if drift_indicators["missing_columns"]:
        warnings.append(
            f"Missing expected columns: {drift_indicators['missing_columns']}"
        )
    if drift_indicators["unexpected_columns"]:
        warnings.append(
            f"Unexpected columns present: {drift_indicators['unexpected_columns']}"
        )

    logger.info("Stage 03 quality checks complete.")

    return QualityReport(
        row_count=row_count,
        null_counts=null_counts,
        duplicate_counts=duplicate_counts,
        drift_indicators=drift_indicators,
        warnings=warnings,
    )
