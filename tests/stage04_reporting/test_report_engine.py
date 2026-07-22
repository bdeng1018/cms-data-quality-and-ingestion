"""
Test Suite: Stage 04 Reporting Engine
===============================================================
This module validates the core analytical functions in
`report_engine.py`, ensuring that Stage 04 reporting logic is:

    - deterministic
    - correct
    - stable
    - fully isolated from I/O
    - aligned with Stage 03 metrics

Each test focuses on a single responsibility:
column health, facility health, sparse column detection,
top/bottom facility ranking, and dataset summary construction.

Logging is included to aid debugging during pipeline development.
"""

import logging

import pandas as pd

from src.stage04_reporting.report_engine import (
    compute_column_health,
    compute_dataset_summary,
    compute_facility_health,
    compute_top_bottom_facilities,
    identify_sparse_columns,
)

# ------------------------------------------------------------------------------
# Configure test logger
# ------------------------------------------------------------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("[%(levelname)s] test_report_engine: %(message)s")
    )
    logger.addHandler(handler)


# ------------------------------------------------------------------------------
# Column Health Tests
# ------------------------------------------------------------------------------
def test_compute_column_health_basic():
    """
    Validate column health classification and notes generation.
    Ensures:
        - completeness → correct health category
        - notes reflect sparsity and dtype issues
    """
    logger.info("Running test_compute_column_health_basic...")

    column_profiles = {
        "colA": {
            "completeness_score": 1.0,
            "distinct_count": 10,
            "inferred_dtype": "str",
        },
        "colB": {
            "completeness_score": 0.0,
            "distinct_count": 0,
            "inferred_dtype": "float64",
        },
    }

    result = compute_column_health(column_profiles)

    assert result["colA"]["health"] == "healthy"
    assert result["colB"]["health"] == "critical"
    assert "column is fully null" in result["colB"]["notes"]

    logger.info("✓ Column health classification validated.")


# ------------------------------------------------------------------------------
# Facility Health Tests
# ------------------------------------------------------------------------------
def test_compute_facility_health_basic():
    """
    Validate facility-level health classification based on completeness.
    """
    logger.info("Running test_compute_facility_health_basic...")

    df = pd.DataFrame(
        {
            "facility_id": ["A", "B"],
            "completeness_score": [0.9, 0.2],
        }
    )

    out = compute_facility_health(df)

    assert out.loc[0, "health"] == "moderate"
    assert out.loc[1, "health"] == "sparse"

    logger.info("✓ Facility health classification validated.")


# ------------------------------------------------------------------------------
# Sparse Column Detection Tests
# ------------------------------------------------------------------------------
def test_identify_sparse_columns():
    """
    Validate identification of sparse and critical columns.
    """
    logger.info("Running test_identify_sparse_columns...")

    column_health = {
        "colA": {"health": "healthy"},
        "colB": {"health": "sparse"},
        "colC": {"health": "critical"},
    }

    sparse = identify_sparse_columns(column_health)

    assert sparse == ["colB", "colC"]

    logger.info("✓ Sparse column detection validated.")


# ------------------------------------------------------------------------------
# Top/Bottom Facility Ranking Tests
# ------------------------------------------------------------------------------
def test_compute_top_bottom_facilities():
    """
    Validate ranking of facilities by completeness score.
    """
    logger.info("Running test_compute_top_bottom_facilities...")

    df = pd.DataFrame(
        {
            "facility_id": ["A", "B", "C"],
            "completeness_score": [0.9, 0.5, 0.1],
        }
    )

    top, bottom = compute_top_bottom_facilities(df, n=1)

    assert top.iloc[0]["facility_id"] == "A"
    assert bottom.iloc[0]["facility_id"] == "C"

    logger.info("✓ Facility ranking validated.")


# ------------------------------------------------------------------------------
# Dataset Summary Tests
# ------------------------------------------------------------------------------
def test_compute_dataset_summary():
    """
    Validate dataset-level summary construction, including:
        - completeness
        - quality
        - column health distribution
    """
    logger.info("Running test_compute_dataset_summary...")

    quality_summary = {
        "total_rows": 100,
        "column_count": 10,
        "facility_count": 100,
        "completeness_score": 0.25,
        "quality_score": 0.25,
    }

    column_health = {
        "colA": {"health": "healthy"},
        "colB": {"health": "critical"},
        "colC": {"health": "moderate"},
    }

    summary = compute_dataset_summary(quality_summary, column_health)

    assert summary["total_rows"] == 100
    assert summary["column_health_distribution"]["healthy"] == 1
    assert summary["column_health_distribution"]["critical"] == 1
    assert summary["column_health_distribution"]["moderate"] == 1

    logger.info("✓ Dataset summary validated.")
