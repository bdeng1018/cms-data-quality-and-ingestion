"""
Stage 04 Reporting Engine
================================================================================
Transforms Stage 03 quality artifacts into structured reporting objects.

Inputs (from stage03_intermediate/):
    - quality_summary.json
    - column_profiles.json
    - facility_metrics.csv

Outputs (returned to report_formatter/report_writer):
    - dataset_summary (dict)
    - column_health (dict)
    - facility_health (DataFrame)
    - sparse_columns (list)
    - top_facilities (DataFrame)
    - bottom_facilities (DataFrame)

Design principles:
    - Pure functions (no I/O)
    - Deterministic, testable logic
    - Clear separation between analysis, formatting, and writing
"""

import json
from pathlib import Path

import pandas as pd

# ==============================================================================
# Loaders (pure, deterministic)
# ==============================================================================


def load_quality_summary(path: Path) -> dict:
    with path.open("r") as f:
        return json.load(f)


def load_column_profiles(path: Path) -> dict:
    with path.open("r") as f:
        return json.load(f)


def load_facility_metrics(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


# ==============================================================================
# Column Health Classification
# ==============================================================================


def classify_column_health(completeness: float) -> str:
    if completeness >= 0.95:
        return "healthy"
    elif completeness >= 0.50:
        return "moderate"
    elif completeness >= 0.10:
        return "sparse"
    return "critical"


def compute_column_health(column_profiles: dict) -> dict:
    """
    Returns:
        {
            column_name: {
                "completeness": float,
                "health": str,
                "distinct_count": int,
                "dtype": str,
                "notes": str
            }
        }
    """
    results = {}

    for col, metrics in column_profiles.items():
        completeness = metrics.get("completeness_score", 0.0)
        health = classify_column_health(completeness)

        notes = []
        if completeness == 0:
            notes.append("column is fully null")
        if metrics.get("distinct_count", 0) == 0:
            notes.append("no distinct values")
        if metrics.get("inferred_dtype") in ("float64", "object") and completeness > 0:
            notes.append("dtype may be inconsistent")

        results[col] = {
            "completeness": completeness,
            "health": health,
            "distinct_count": metrics.get("distinct_count"),
            "dtype": metrics.get("inferred_dtype"),
            "notes": "; ".join(notes) if notes else "",
        }

    return results


# ==============================================================================
# Facility Health Classification
# ==============================================================================


def classify_facility_health(completeness: float) -> str:
    if completeness >= 0.95:
        return "healthy"
    elif completeness >= 0.50:
        return "moderate"
    elif completeness >= 0.10:
        return "sparse"
    return "critical"


def compute_facility_health(df_facility: pd.DataFrame) -> pd.DataFrame:
    df = df_facility.copy()
    df["health"] = df["completeness_score"].apply(classify_facility_health)
    return df


# ==============================================================================
# Sparse Columns Report
# ==============================================================================


def identify_sparse_columns(column_health: dict) -> list:
    return [
        col
        for col, info in column_health.items()
        if info["health"] in ("sparse", "critical")
    ]


# ==============================================================================
# Top / Bottom Facilities
# ==============================================================================


def compute_top_bottom_facilities(df_facility: pd.DataFrame, n: int = 25):
    df_sorted = df_facility.sort_values("completeness_score", ascending=False)
    top = df_sorted.head(n)
    bottom = df_sorted.tail(n)
    return top, bottom


# ==============================================================================
# Dataset Summary
# ==============================================================================


def compute_dataset_summary(quality_summary: dict, column_health: dict) -> dict:
    health_counts = {
        "healthy": 0,
        "moderate": 0,
        "sparse": 0,
        "critical": 0,
    }

    for info in column_health.values():
        health_counts[info["health"]] += 1

    return {
        "total_rows": quality_summary.get("total_rows"),
        "column_count": quality_summary.get("column_count"),
        "facility_count": quality_summary.get("facility_count"),
        "dataset_completeness": quality_summary.get("completeness_score"),
        "dataset_quality": quality_summary.get("quality_score"),
        "column_health_distribution": health_counts,
    }


# ==============================================================================
# Main Engine API (called by run_reporting.py)
# ==============================================================================


def run_report_engine(
    quality_summary_path: Path,
    column_profiles_path: Path,
    facility_metrics_path: Path,
):
    """
    Returns a dictionary of structured reporting objects.
    No I/O beyond reading Stage 03 artifacts.
    """

    quality_summary = load_quality_summary(quality_summary_path)
    column_profiles = load_column_profiles(column_profiles_path)
    df_facility = load_facility_metrics(facility_metrics_path)

    column_health = compute_column_health(column_profiles)
    facility_health = compute_facility_health(df_facility)
    sparse_columns = identify_sparse_columns(column_health)
    top_facilities, bottom_facilities = compute_top_bottom_facilities(df_facility)
    dataset_summary = compute_dataset_summary(quality_summary, column_health)

    return {
        "dataset_summary": dataset_summary,
        "column_health": column_health,
        "facility_health": facility_health,
        "sparse_columns": sparse_columns,
        "top_facilities": top_facilities,
        "bottom_facilities": bottom_facilities,
    }
