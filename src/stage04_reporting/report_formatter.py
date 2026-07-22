"""
Stage 04 Report Formatter
================================================================================
Converts structured reporting objects from the Stage 04 engine into
JSON‑serializable dictionaries and CSV‑ready DataFrames.

Design principles:
    - No I/O (writer handles file output)
    - Pure transformations
    - Deterministic and testable
"""

import pandas as pd

# ==============================================================================
# JSON Formatters
# ==============================================================================


def format_dataset_summary(dataset_summary: dict) -> dict:
    """
    Ensure dataset summary is JSON‑serializable.
    """
    return {
        "total_rows": dataset_summary["total_rows"],
        "column_count": dataset_summary["column_count"],
        "facility_count": dataset_summary["facility_count"],
        "dataset_completeness": dataset_summary["dataset_completeness"],
        "dataset_quality": dataset_summary["dataset_quality"],
        "column_health_distribution": dataset_summary["column_health_distribution"],
    }


def format_column_health(column_health: dict) -> dict:
    """
    Column health is already JSON‑friendly, but we ensure consistent structure.
    """
    formatted = {}
    for col, info in column_health.items():
        formatted[col] = {
            "completeness": float(info["completeness"]),
            "health": info["health"],
            "distinct_count": (
                int(info["distinct_count"])
                if info["distinct_count"] is not None
                else None
            ),
            "dtype": info["dtype"],
            "notes": info["notes"],
        }
    return formatted


def format_sparse_columns(sparse_columns: list) -> dict:
    """
    Wrap sparse columns list in a JSON‑friendly structure.
    """
    return {"sparse_columns": sparse_columns}


# ==============================================================================
# CSV Formatters
# ==============================================================================


def format_facility_health(df_facility: pd.DataFrame) -> pd.DataFrame:
    """
    Facility health is already a DataFrame — return a clean copy.
    """
    return df_facility.copy()


def format_top_bottom_facilities(top_df: pd.DataFrame, bottom_df: pd.DataFrame):
    """
    Return clean DataFrames for writing.
    """
    return top_df.copy(), bottom_df.copy()


# ==============================================================================
# Main Formatter API (called by report_writer.py)
# ==============================================================================


def format_reports(report_objects: dict):
    """
    Accepts the dictionary returned by run_report_engine() and returns
    a dictionary of formatted objects ready for writing.

    Input keys:
        - dataset_summary
        - column_health
        - facility_health
        - sparse_columns
        - top_facilities
        - bottom_facilities
    """

    return {
        "dataset_summary_json": format_dataset_summary(
            report_objects["dataset_summary"]
        ),
        "column_health_json": format_column_health(report_objects["column_health"]),
        "sparse_columns_json": format_sparse_columns(report_objects["sparse_columns"]),
        "facility_health_csv": format_facility_health(
            report_objects["facility_health"]
        ),
        "top_facilities_csv": report_objects["top_facilities"].copy(),
        "bottom_facilities_csv": report_objects["bottom_facilities"].copy(),
    }
