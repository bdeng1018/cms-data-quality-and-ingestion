"""
Stage 03 Quality Engine
================================================================================
Pure computation module for Stage 03 of the CMS POS/QIES ingestion pipeline.

Responsibilities:
    - dataset-level metrics
    - facility-level metrics
    - column-level profiles

Design principles:
    - Pure computation only (no writing, no filesystem)
    - Strong typing and explicit data contracts
    - Structured logging for pipeline observability
    - Stage 03 runner handles persistence
"""

import logging
from typing import Any, Dict, Tuple

import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] stage03_quality_engine: %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)


# ==============================================================================
# Dataset-level metrics
# ==============================================================================
def compute_dataset_metrics(df: pd.DataFrame, schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute dataset-level quality metrics.

    Returns a dictionary containing:
        - total_rows
        - column_count
        - facility_count
        - missingness_summary
        - completeness_score
        - quality_score
    """
    logger.info("Computing dataset-level metrics...")

    total_rows = len(df)
    column_count = len(df.columns)
    facility_count = (
        df["facility_id"].nunique() if "facility_id" in df.columns else None
    )

    missingness_summary = df.isna().sum().to_dict()

    # Placeholder scoring logic (Branch 1)
    completeness_score = 1.0 - (
        sum(missingness_summary.values()) / (total_rows * column_count)
    )
    quality_score = completeness_score

    summary = {
        "total_rows": total_rows,
        "column_count": column_count,
        "facility_count": facility_count,
        "missingness_summary": missingness_summary,
        "completeness_score": completeness_score,
        "quality_score": quality_score,
    }

    logger.info("Dataset-level metrics computed.")
    return summary


# ==============================================================================
# Facility-level metrics
# ==============================================================================
def compute_facility_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute facility-level metrics.

    Returns a DataFrame containing:
        - facility_id
        - row_count
        - missingness_rate
        - completeness_score
        - quality_score
    """
    logger.info("Computing facility-level metrics...")

    if "facility_id" not in df.columns:
        raise ValueError("Missing required column: facility_id")

    facility_groups = df.groupby("facility_id")

    records = []
    for facility_id, group in facility_groups:
        row_count = len(group)
        missingness_rate = group.isna().sum().sum() / (row_count * len(group.columns))

        completeness_score = 1.0 - missingness_rate
        quality_score = completeness_score

        records.append(
            {
                "facility_id": facility_id,
                "row_count": row_count,
                "missingness_rate": missingness_rate,
                "completeness_score": completeness_score,
                "quality_score": quality_score,
            }
        )

    df_facility = pd.DataFrame(records)
    logger.info("Facility-level metrics computed.")
    return df_facility


# ==============================================================================
# Column-level profiles
# ==============================================================================
def compute_column_profiles(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    Compute column-level profiles.

    Returns a dictionary keyed by column name containing:
        - null_count
        - distinct_count
        - min_value
        - max_value
        - inferred_dtype
        - completeness_score
        - quality_score
    """
    logger.info("Computing column-level profiles...")

    profiles = {}

    for col in df.columns:
        series = df[col]

        null_count = series.isna().sum()
        distinct_count = series.nunique(dropna=True)
        inferred_dtype = str(series.dtype)

        completeness_score = 1.0 - (null_count / len(series))
        quality_score = completeness_score

        profiles[col] = {
            "null_count": null_count,
            "distinct_count": distinct_count,
            "min_value": (
                series.min() if pd.api.types.is_numeric_dtype(series) else None
            ),
            "max_value": (
                series.max() if pd.api.types.is_numeric_dtype(series) else None
            ),
            "inferred_dtype": inferred_dtype,
            "completeness_score": completeness_score,
            "quality_score": quality_score,
        }

    logger.info("Column-level profiles computed.")
    return profiles


# ==============================================================================
# Stage 03 orchestrator (pure computation)
# ==============================================================================
def run_stage03_quality(
    df: pd.DataFrame, schema: Dict[str, Any]
) -> Tuple[Dict[str, Any], pd.DataFrame, Dict[str, Dict[str, Any]]]:
    """
    Run the full Stage 03 quality pipeline.

    Returns
    -------
    summary_dict : Dict[str, Any]
    df_facility : pd.DataFrame
    column_profiles : Dict[str, Dict[str, Any]]

    Notes
    -----
    - Pure computation only.
    - Stage 03 runner handles persistence.
    """
    logger.info("Starting Stage 03 quality pipeline...")

    summary_dict = compute_dataset_metrics(df, schema)
    df_facility = compute_facility_metrics(df)
    column_profiles = compute_column_profiles(df)

    logger.info("Stage 03 quality pipeline completed successfully.")
    return summary_dict, df_facility, column_profiles
