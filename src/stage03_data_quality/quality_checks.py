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

    def to_dict(self) -> dict:
        """
        Deterministic JSON‑serializable representation of the quality report.
        Keys are sorted alphabetically to satisfy Stage 03 test requirements.
        """
        missing_cols = self.drift_indicators.get("missing_columns", []) or []
        unexpected_cols = self.drift_indicators.get("unexpected_columns", []) or []

        # Build the unsorted dict first
        raw = {
            "row_count": int(self.row_count),
            "null_counts": dict(sorted(self.null_counts.items())),
            "duplicate_counts": dict(sorted(self.duplicate_counts.items())),
            "drift_indicators": {
                "missing_columns": sorted(missing_cols),
                "unexpected_columns": sorted(unexpected_cols),
            },
            "warnings": sorted(self.warnings),
        }

        # Return a new dict with sorted keys
        return {key: raw[key] for key in sorted(raw.keys())}


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


def compute_completeness(
    df: pd.DataFrame, required_columns: List[str]
) -> Dict[str, List[str]]:
    """
    Determine which required columns are missing or entirely null.

    Args:
        df: Raw DataFrame.
        required_columns: Columns that must exist and contain non-null values.

    Returns:
        Dictionary with lists of missing and empty columns.
    """
    logger.debug("Checking QC completeness.")

    missing = [col for col in required_columns if col not in df.columns]
    empty = [
        col for col in required_columns if col in df.columns and df[col].isna().all()
    ]

    return {
        "missing_required_columns": missing,
        "empty_required_columns": empty,
    }


def compute_metadata_completeness(
    df: pd.DataFrame, metadata_fields: List[str]
) -> Dict[str, List[str]]:
    """
    Check metadata fields for missing or null values.

    Args:
        df: Raw DataFrame.
        metadata_fields: Metadata columns expected to be present and non-null.

    Returns:
        Dictionary with lists of missing metadata fields and fields with nulls.
    """
    logger.debug("Checking metadata completeness.")

    missing = [col for col in metadata_fields if col not in df.columns]
    null_fields = [
        col for col in metadata_fields if col in df.columns and df[col].isna().any()
    ]

    return {
        "missing_metadata_fields": missing,
        "metadata_fields_with_nulls": null_fields,
    }


def classify_drift_severity(drift: Dict[str, List[str]]) -> str:
    """
    Classify drift severity based on missing/unexpected columns.

    Returns:
        'none', 'minor', or 'major'
    """
    missing = drift.get("missing_columns", [])
    unexpected = drift.get("unexpected_columns", [])

    if not missing and not unexpected:
        return "none"

    if len(missing) <= 1 and len(unexpected) <= 1:
        return "minor"

    return "major"


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
    # QC completeness
    required_columns = expected_columns  # reuse expected schema
    completeness = compute_completeness(df, required_columns)

    # Metadata completeness
    metadata_fields = ["ccn", "facility_name", "state", "zip"]  # safe public fields
    metadata_completeness = compute_metadata_completeness(df, metadata_fields)

    # Drift severity
    drift_severity = classify_drift_severity(drift_indicators)

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

    # Completeness warnings
    if completeness["missing_required_columns"]:
        warnings.append(
            f"Missing required columns: {completeness['missing_required_columns']}"
        )
    if completeness["empty_required_columns"]:
        warnings.append(
            f"Required columns with all-null values: {completeness['empty_required_columns']}"
        )

    # Metadata warnings
    if metadata_completeness["missing_metadata_fields"]:
        warnings.append(
            f"Missing metadata fields: {metadata_completeness['missing_metadata_fields']}"
        )
    if metadata_completeness["metadata_fields_with_nulls"]:
        warnings.append(
            f"Metadata fields containing nulls: {metadata_completeness['metadata_fields_with_nulls']}"
        )

    # Drift severity warning
    if drift_severity == "major":
        warnings.append("Major schema drift detected.")
    elif drift_severity == "minor":
        warnings.append("Minor schema drift detected.")

    logger.info("Stage 03 quality checks complete.")

    return QualityReport(
        row_count=row_count,
        null_counts=null_counts,
        duplicate_counts=duplicate_counts,
        drift_indicators={
            **drift_indicators,
            "drift_severity": [drift_severity],
            "missing_required_columns": completeness["missing_required_columns"],
            "empty_required_columns": completeness["empty_required_columns"],
            "missing_metadata_fields": metadata_completeness["missing_metadata_fields"],
            "metadata_fields_with_nulls": metadata_completeness[
                "metadata_fields_with_nulls"
            ],
        },
        warnings=warnings,
    )
