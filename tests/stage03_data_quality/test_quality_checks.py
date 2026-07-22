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
