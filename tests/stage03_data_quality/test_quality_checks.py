"""
Tests for Stage 03 — quality_checks.py

These tests validate:
    - module imports
    - QualityReport structure
    - null count computation
    - duplicate detection
    - drift indicators
    - warnings behavior

This suite is intentionally lightweight for Branch 1 MVP.
"""

import pandas as pd

from src.stage03_data_quality.quality_checks import (
    QualityReport,
    run_quality_checks,
)

# import pytest


def test_imports():
    assert QualityReport is not None
    assert callable(run_quality_checks)


def test_quality_report_structure():
    df = pd.DataFrame({"ccn": [1, 2], "provider_type": ["A", "B"]})
    expected_cols = ["ccn", "provider_type"]

    report = run_quality_checks(df, expected_cols, key="ccn")

    assert isinstance(report, QualityReport)
    assert isinstance(report.row_count, int)
    assert isinstance(report.null_counts, dict)
    assert isinstance(report.duplicate_counts, dict)
    assert isinstance(report.drift_indicators, dict)
    assert isinstance(report.warnings, list)
    assert "drift_severity" in report.drift_indicators
    assert "missing_required_columns" in report.drift_indicators
    assert "empty_required_columns" in report.drift_indicators
    assert "missing_metadata_fields" in report.drift_indicators
    assert "metadata_fields_with_nulls" in report.drift_indicators


def test_null_counts():
    df = pd.DataFrame(
        {
            "ccn": [1, None, 3],
            "provider_type": ["A", "B", None],
        }
    )
    expected_cols = ["ccn", "provider_type"]

    report = run_quality_checks(df, expected_cols, key="ccn")

    assert report.null_counts["ccn"] == 1
    assert report.null_counts["provider_type"] == 1


def test_duplicate_detection():
    df = pd.DataFrame(
        {
            "ccn": [100, 100, 200],
            "provider_type": ["A", "A", "B"],
        }
    )
    expected_cols = ["ccn", "provider_type"]

    report = run_quality_checks(df, expected_cols, key="ccn")

    assert report.duplicate_counts["ccn"] == 1
    assert any("Duplicate" in w for w in report.warnings)


def test_drift_detection_missing_columns():
    df = pd.DataFrame({"ccn": [1, 2]})
    expected_cols = ["ccn", "provider_type"]

    report = run_quality_checks(df, expected_cols, key="ccn")

    assert "provider_type" in report.drift_indicators["missing_columns"]
    assert any("Missing expected columns" in w for w in report.warnings)
    assert report.drift_indicators["drift_severity"] == ["minor"]


def test_drift_detection_unexpected_columns():
    df = pd.DataFrame(
        {
            "ccn": [1, 2],
            "provider_type": ["A", "B"],
            "extra_col": [10, 20],
        }
    )
    expected_cols = ["ccn", "provider_type"]

    report = run_quality_checks(df, expected_cols, key="ccn")

    assert "extra_col" in report.drift_indicators["unexpected_columns"]
    assert any("Unexpected columns" in w for w in report.warnings)
    assert report.drift_indicators["drift_severity"] == ["minor"]


# --- Deterministic behavior tests for Stage 03 quality_checks.py ---


def test_quality_checks_are_deterministic():
    """Repeated calls must produce identical QualityReport objects."""
    df = pd.DataFrame(
        {
            "ccn": [1, None, 3],
            "provider_type": ["A", "B", None],
        }
    )
    expected_cols = ["ccn", "provider_type"]

    r1 = run_quality_checks(df, expected_cols, key="ccn")
    r2 = run_quality_checks(df, expected_cols, key="ccn")

    # Deterministic row count
    assert r1.row_count == r2.row_count, "row_count must be deterministic"

    # Deterministic null counts
    assert r1.null_counts == r2.null_counts, "null_counts must be deterministic"

    # Deterministic duplicate counts
    assert (
        r1.duplicate_counts == r2.duplicate_counts
    ), "duplicate_counts must be deterministic"

    # Deterministic drift indicators
    assert (
        r1.drift_indicators == r2.drift_indicators
    ), "drift_indicators must be deterministic"

    # Deterministic warnings
    assert r1.warnings == r2.warnings, "warnings list must be deterministic"

    assert (
        r1.drift_indicators["drift_severity"] == r2.drift_indicators["drift_severity"]
    )
    assert (
        r1.drift_indicators["missing_required_columns"]
        == r2.drift_indicators["missing_required_columns"]
    )
    assert (
        r1.drift_indicators["empty_required_columns"]
        == r2.drift_indicators["empty_required_columns"]
    )
    assert (
        r1.drift_indicators["missing_metadata_fields"]
        == r2.drift_indicators["missing_metadata_fields"]
    )
    assert (
        r1.drift_indicators["metadata_fields_with_nulls"]
        == r2.drift_indicators["metadata_fields_with_nulls"]
    )


def test_null_counts_key_order_is_deterministic():
    """null_counts keys must be sorted deterministically."""
    df = pd.DataFrame(
        {
            "ccn": [1, None],
            "provider_type": ["A", None],
        }
    )
    expected_cols = ["ccn", "provider_type"]

    report = run_quality_checks(df, expected_cols, key="ccn")
    keys = list(report.null_counts.keys())

    assert keys == sorted(keys), "null_counts keys must be sorted deterministically"


def test_duplicate_counts_key_order_is_deterministic():
    """duplicate_counts keys must be sorted deterministically."""
    df = pd.DataFrame(
        {
            "ccn": [100, 100, 200],
            "provider_type": ["A", "A", "B"],
        }
    )
    expected_cols = ["ccn", "provider_type"]

    report = run_quality_checks(df, expected_cols, key="ccn")
    keys = list(report.duplicate_counts.keys())

    assert keys == sorted(
        keys
    ), "duplicate_counts keys must be sorted deterministically"


def test_warnings_are_deterministic_and_sorted():
    """Warnings must be deterministic and sorted for reproducibility."""
    df = pd.DataFrame(
        {
            "ccn": [100, 100, 200],
            "provider_type": ["A", "A", "B"],
        }
    )
    expected_cols = ["ccn", "provider_type"]

    report = run_quality_checks(df, expected_cols, key="ccn")

    assert report.warnings == sorted(
        report.warnings
    ), "warnings must be sorted deterministically"


def test_drift_indicators_are_deterministic():
    """Drift indicators must be deterministic across repeated calls."""
    df = pd.DataFrame({"ccn": [1, 2]})
    expected_cols = ["ccn", "provider_type"]

    r1 = run_quality_checks(df, expected_cols, key="ccn")
    r2 = run_quality_checks(df, expected_cols, key="ccn")

    assert (
        r1.drift_indicators == r2.drift_indicators
    ), "drift_indicators must be deterministic"
    assert (
        r1.drift_indicators["drift_severity"] == r2.drift_indicators["drift_severity"]
    )


def test_quality_report_serializable_deterministically():
    """QualityReport must be JSON‑serializable in a deterministic structure."""
    df = pd.DataFrame({"ccn": [1, None], "provider_type": ["A", None]})
    expected_cols = ["ccn", "provider_type"]

    report = run_quality_checks(df, expected_cols, key="ccn")
    serialized = report.to_dict()

    # Required deterministic keys
    required = {
        "row_count",
        "null_counts",
        "duplicate_counts",
        "drift_indicators",
        "warnings",
    }

    missing = required - set(serialized.keys())
    assert not missing, f"Missing keys in serialized QualityReport: {missing}"

    # Deterministic ordering of top-level keys
    assert list(serialized.keys()) == sorted(
        serialized.keys()
    ), "Serialized QualityReport keys must be sorted deterministically"
    assert "drift_severity" in report.drift_indicators


def test_completeness_and_metadata_completeness():
    df = pd.DataFrame(
        {
            "ccn": [None, None],
            "provider_type": ["A", "B"],
            "state": [None, None],
            # facility_name and zip missing entirely
        }
    )

    expected_cols = ["ccn", "provider_type"]

    report = run_quality_checks(df, expected_cols, key="ccn")

    # Required columns
    assert "ccn" in report.drift_indicators["empty_required_columns"]
    assert "provider_type" not in report.drift_indicators["empty_required_columns"]

    # Metadata completeness
    assert "facility_name" in report.drift_indicators["missing_metadata_fields"]
    assert "zip" in report.drift_indicators["missing_metadata_fields"]
    assert "state" in report.drift_indicators["metadata_fields_with_nulls"]
