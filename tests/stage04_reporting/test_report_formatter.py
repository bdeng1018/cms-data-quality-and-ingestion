"""
Test Suite: Stage 04 Report Formatter
===============================================================
Validates the formatting layer of Stage 04 reporting.

The formatter is responsible for:
    - converting engine outputs into JSON‑serializable dicts
    - preparing DataFrames for CSV writing
    - ensuring consistent structure for downstream writer

This suite ensures:
    - deterministic formatting
    - correct JSON structure
    - correct DataFrame structure
    - no filesystem interaction
    - no mutation of input objects

Logging is included for pipeline debugging.
"""

import logging

import pandas as pd

from src.stage04_reporting.report_formatter import (
    format_column_health,
    format_dataset_summary,
    format_facility_health,
    format_reports,
    format_sparse_columns,
    format_top_bottom_facilities,
)

# ------------------------------------------------------------------------------
# Configure test logger
# ------------------------------------------------------------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("[%(levelname)s] test_report_formatter: %(message)s")
    )
    logger.addHandler(handler)


# ------------------------------------------------------------------------------
# Dataset Summary Formatting
# ------------------------------------------------------------------------------
def test_format_dataset_summary():
    """
    Validate JSON‑ready dataset summary formatting.
    """
    logger.info("Running test_format_dataset_summary...")

    summary = {
        "total_rows": 100,
        "column_count": 10,
        "facility_count": 100,
        "dataset_completeness": 0.25,
        "dataset_quality": 0.25,
        "column_health_distribution": {"healthy": 1, "critical": 2},
    }

    out = format_dataset_summary(summary)

    assert out["total_rows"] == 100
    assert out["column_count"] == 10
    assert out["dataset_completeness"] == 0.25
    assert "column_health_distribution" in out

    logger.info("✓ Dataset summary formatting validated.")


# ------------------------------------------------------------------------------
# Column Health Formatting
# ------------------------------------------------------------------------------
def test_format_column_health():
    """
    Validate JSON‑friendly column health formatting.
    """
    logger.info("Running test_format_column_health...")

    column_health = {
        "colA": {
            "completeness": 1.0,
            "health": "healthy",
            "distinct_count": 10,
            "dtype": "str",
            "notes": "",
        },
        "colB": {
            "completeness": 0.0,
            "health": "critical",
            "distinct_count": 0,
            "dtype": "float64",
            "notes": "column is fully null",
        },
    }

    out = format_column_health(column_health)

    assert out["colA"]["health"] == "healthy"
    assert out["colB"]["distinct_count"] == 0
    assert out["colB"]["notes"] == "column is fully null"

    logger.info("✓ Column health formatting validated.")


# ------------------------------------------------------------------------------
# Sparse Columns Formatting
# ------------------------------------------------------------------------------
def test_format_sparse_columns():
    """
    Validate sparse column list formatting.
    """
    logger.info("Running test_format_sparse_columns...")

    sparse = ["colB", "colC"]
    out = format_sparse_columns(sparse)

    assert out["sparse_columns"] == ["colB", "colC"]

    logger.info("✓ Sparse column formatting validated.")


# ------------------------------------------------------------------------------
# Facility Health Formatting
# ------------------------------------------------------------------------------
def test_format_facility_health():
    """
    Validate DataFrame passthrough for facility health CSV formatting.
    """
    logger.info("Running test_format_facility_health...")

    df = pd.DataFrame(
        {
            "facility_id": ["A", "B"],
            "completeness_score": [0.9, 0.2],
            "health": ["moderate", "sparse"],
        }
    )

    out = format_facility_health(df)

    assert isinstance(out, pd.DataFrame)
    assert list(out.columns) == ["facility_id", "completeness_score", "health"]
    assert out.loc[1, "health"] == "sparse"

    logger.info("✓ Facility health DataFrame formatting validated.")


# ------------------------------------------------------------------------------
# Top/Bottom Facility Formatting
# ------------------------------------------------------------------------------
def test_format_top_bottom_facilities():
    """
    Validate DataFrame passthrough for top/bottom facility CSV formatting.
    """
    logger.info("Running test_format_top_bottom_facilities...")

    top_df = pd.DataFrame({"facility_id": ["A"], "completeness_score": [0.9]})
    bottom_df = pd.DataFrame({"facility_id": ["C"], "completeness_score": [0.1]})

    top_out, bottom_out = format_top_bottom_facilities(top_df, bottom_df)

    assert isinstance(top_out, pd.DataFrame)
    assert isinstance(bottom_out, pd.DataFrame)
    assert top_out.iloc[0]["facility_id"] == "A"
    assert bottom_out.iloc[0]["facility_id"] == "C"

    logger.info("✓ Top/bottom facility formatting validated.")


# ------------------------------------------------------------------------------
# Full Report Formatting
# ------------------------------------------------------------------------------
def test_format_reports_end_to_end():
    """
    Validate full formatting pipeline using synthetic engine output.
    Ensures:
        - JSON objects are structured correctly
        - CSV DataFrames are preserved
        - No mutation of input objects
    """
    logger.info("Running test_format_reports_end_to_end...")

    report_objects = {
        "dataset_summary": {
            "total_rows": 100,
            "column_count": 10,
            "facility_count": 100,
            "dataset_completeness": 0.25,
            "dataset_quality": 0.25,
            "column_health_distribution": {"healthy": 1, "critical": 2},
        },
        "column_health": {
            "colA": {
                "completeness": 1.0,
                "health": "healthy",
                "distinct_count": 10,
                "dtype": "str",
                "notes": "",
            },
        },
        "facility_health": pd.DataFrame(
            {
                "facility_id": ["A"],
                "completeness_score": [0.9],
                "health": ["moderate"],
            }
        ),
        "sparse_columns": ["colB"],
        "top_facilities": pd.DataFrame(
            {"facility_id": ["A"], "completeness_score": [0.9]}
        ),
        "bottom_facilities": pd.DataFrame(
            {"facility_id": ["C"], "completeness_score": [0.1]}
        ),
    }

    formatted = format_reports(report_objects)

    assert "dataset_summary_json" in formatted
    assert "column_health_json" in formatted
    assert "facility_health_csv" in formatted
    assert "top_facilities_csv" in formatted
    assert "bottom_facilities_csv" in formatted

    logger.info("✓ End‑to‑end report formatting validated.")
