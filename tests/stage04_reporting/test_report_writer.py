"""
Test Suite: Stage 04 Report Writer
===============================================================
Validates the file‑writing layer of Stage 04 reporting.

The writer is responsible for:
    - writing JSON artifacts
    - writing CSV artifacts
    - generating a report index manifest
    - ensuring directories exist

This suite ensures:
    - correct file creation
    - correct JSON/CSV content
    - safe writing into a temporary test directory
    - no interaction with real pipeline data directories

Logging is included for debugging and CI visibility.
"""

import json
import logging

import pandas as pd

from src.stage04_reporting.report_writer import write_reports

# from pathlib import Path


# ------------------------------------------------------------------------------
# Configure test logger
# ------------------------------------------------------------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("[%(levelname)s] test_report_writer: %(message)s")
    )
    logger.addHandler(handler)


# ------------------------------------------------------------------------------
# Helper: Create synthetic formatted reports
# ------------------------------------------------------------------------------
def _synthetic_formatted_reports():
    """
    Returns a synthetic formatted report dictionary identical in structure
    to what `format_reports()` produces.
    """
    return {
        "dataset_summary_json": {
            "total_rows": 100,
            "column_count": 10,
            "facility_count": 100,
            "dataset_completeness": 0.25,
            "dataset_quality": 0.25,
            "column_health_distribution": {"healthy": 1, "critical": 2},
        },
        "column_health_json": {
            "colA": {
                "completeness": 1.0,
                "health": "healthy",
                "distinct_count": 10,
                "dtype": "str",
                "notes": "",
            }
        },
        "sparse_columns_json": {"sparse_columns": ["colB"]},
        "facility_health_csv": pd.DataFrame(
            {
                "facility_id": ["A"],
                "completeness_score": [0.9],
                "health": ["moderate"],
            }
        ),
        "top_facilities_csv": pd.DataFrame(
            {
                "facility_id": ["A"],
                "completeness_score": [0.9],
            }
        ),
        "bottom_facilities_csv": pd.DataFrame(
            {
                "facility_id": ["C"],
                "completeness_score": [0.1],
            }
        ),
    }


# ------------------------------------------------------------------------------
# Main Writer Tests
# ------------------------------------------------------------------------------
def test_write_reports(tmp_path):
    """
    Validate that Stage 04 writer:
        - creates JSON files
        - creates CSV files
        - writes correct content
        - generates a report index manifest
        - does NOT touch real pipeline directories

    Uses pytest's tmp_path fixture to ensure safe, isolated filesystem writes.
    """
    logger.info("Running test_write_reports...")

    # Synthetic formatted reports
    formatted = _synthetic_formatted_reports()

    # Write into temporary directory
    output_dir = tmp_path / "stage04_test_output"
    output_dir.mkdir()

    _ = write_reports(formatted, base_dir=output_dir)

    # ----------------------------------------------------------------------
    # Validate JSON artifacts
    # ----------------------------------------------------------------------
    dataset_summary_path = output_dir / "dataset_summary.json"
    column_health_path = output_dir / "column_health.json"
    sparse_columns_path = output_dir / "sparse_columns.json"
    report_index_path = output_dir / "report_index.json"

    assert dataset_summary_path.exists()
    assert column_health_path.exists()
    assert sparse_columns_path.exists()
    assert report_index_path.exists()

    # Validate JSON content loads correctly
    with dataset_summary_path.open("r") as f:
        ds = json.load(f)
    assert ds["total_rows"] == 100

    with column_health_path.open("r") as f:
        ch = json.load(f)
    assert "colA" in ch

    with sparse_columns_path.open("r") as f:
        sc = json.load(f)
    assert sc["sparse_columns"] == ["colB"]

    # ----------------------------------------------------------------------
    # Validate CSV artifacts
    # ----------------------------------------------------------------------
    facility_health_path = output_dir / "facility_health.csv"
    top_facilities_path = output_dir / "top_facilities.csv"
    bottom_facilities_path = output_dir / "bottom_facilities.csv"

    assert facility_health_path.exists()
    assert top_facilities_path.exists()
    assert bottom_facilities_path.exists()

    df_fac = pd.read_csv(facility_health_path)
    assert df_fac.iloc[0]["facility_id"] == "A"

    df_top = pd.read_csv(top_facilities_path)
    assert df_top.iloc[0]["facility_id"] == "A"

    df_bottom = pd.read_csv(bottom_facilities_path)
    assert df_bottom.iloc[0]["facility_id"] == "C"

    # ----------------------------------------------------------------------
    # Validate report index manifest
    # ----------------------------------------------------------------------
    with report_index_path.open("r") as f:
        index = json.load(f)

    assert "dataset_summary" in index
    assert "column_health" in index
    assert "facility_health" in index

    logger.info("✓ Stage 04 writer validated successfully.")
