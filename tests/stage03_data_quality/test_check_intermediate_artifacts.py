"""
Tests for Stage 03 Diagnostics — Intermediate Artifact Validation

This version is NON‑DESTRUCTIVE:
    - uses pytest tmp_path for all artifacts
    - monkeypatches diagnostics paths
    - does NOT delete real pipeline directories
"""

import json

import pandas as pd
import pytest

import scripts.diagnostics.stage03.check_intermediate_artifacts as diag

# ==============================================================================
# Helpers
# ==============================================================================


def write_cleaned_data(path):
    df = pd.DataFrame(
        {
            "facility_id": ["A", "A", "B"],
            "col1": [1, 2, None],
            "col2": ["x", None, "z"],
        }
    )
    df.to_csv(path, index=False)


# ==============================================================================
# Fixture — monkeypatch all paths to tmp_path
# ==============================================================================


@pytest.fixture(autouse=True)
def patch_paths(tmp_path, monkeypatch):
    """
    Redirect all Stage 03 diagnostic paths to a temporary directory.
    This prevents tests from deleting real pipeline artifacts.
    """

    intermediate = tmp_path / "stage03_intermediate"
    intermediate.mkdir()

    cleaned = tmp_path / "cleaned_data.csv"

    monkeypatch.setattr(diag, "INTERMEDIATE_DIR", intermediate)
    monkeypatch.setattr(diag, "SUMMARY_PATH", intermediate / "quality_summary.json")
    monkeypatch.setattr(diag, "FACILITY_PATH", intermediate / "facility_metrics.csv")
    monkeypatch.setattr(diag, "PROFILES_PATH", intermediate / "column_profiles.json")
    monkeypatch.setattr(diag, "CLEANED_DATA_PATH", cleaned)

    return {
        "intermediate": intermediate,
        "cleaned": cleaned,
    }


# ==============================================================================
# Tests — quality_summary.json
# ==============================================================================


def test_missing_quality_summary_raises():
    with pytest.raises(FileNotFoundError):
        diag.check_quality_summary()


def test_malformed_quality_summary_raises():
    diag.SUMMARY_PATH.write_text("{bad json}")

    with pytest.raises(Exception):
        diag.check_quality_summary()


def test_valid_quality_summary_passes():
    summary = {
        "total_rows": 3,
        "column_count": 3,
        "missingness_summary": {"col1": 1},
        "quality_score": 0.95,
    }
    with diag.SUMMARY_PATH.open("w") as f:
        json.dump(summary, f)

    diag.check_quality_summary()  # should not raise


# ==============================================================================
# Tests — facility_metrics.csv
# ==============================================================================


def test_missing_facility_metrics_raises():
    with pytest.raises(FileNotFoundError):
        diag.check_facility_metrics()


def test_malformed_facility_metrics_raises():
    diag.FACILITY_PATH.write_text("not,a,csv")

    with pytest.raises(Exception):
        diag.check_facility_metrics()


def test_valid_facility_metrics_passes():
    df = pd.DataFrame(
        {
            "facility_id": ["A", "B"],
            "row_count": [10, 20],
            "missingness_rate": [0.1, 0.2],
            "quality_score": [0.9, 0.8],
        }
    )
    df.to_csv(diag.FACILITY_PATH, index=False)

    diag.check_facility_metrics()  # should not raise


# ==============================================================================
# Tests — column_profiles.json
# ==============================================================================


def test_missing_column_profiles_raises():
    with pytest.raises(FileNotFoundError):
        diag.check_column_profiles()


def test_malformed_column_profiles_raises():
    diag.PROFILES_PATH.write_text("{bad json}")

    with pytest.raises(Exception):
        diag.check_column_profiles()


def test_valid_column_profiles_passes():
    profiles = {
        "col1": {
            "null_count": 1,
            "distinct_count": 2,
            "inferred_dtype": "int64",
            "quality_score": 0.95,
        }
    }
    with diag.PROFILES_PATH.open("w") as f:
        json.dump(profiles, f)

    diag.check_column_profiles()  # should not raise


# ==============================================================================
# Tests — consistency checks
# ==============================================================================


def test_inconsistent_facility_ids_raises():
    write_cleaned_data(diag.CLEANED_DATA_PATH)

    df = pd.DataFrame(
        {
            "facility_id": ["C"],  # not in cleaned data
            "row_count": [10],
            "missingness_rate": [0.1],
            "quality_score": [0.9],
        }
    )
    df.to_csv(diag.FACILITY_PATH, index=False)

    diag.PROFILES_PATH.write_text("{}")
    diag.SUMMARY_PATH.write_text("{}")

    with pytest.raises(ValueError):
        diag.check_consistency_with_cleaned_data()


def test_inconsistent_column_names_raises():
    write_cleaned_data(diag.CLEANED_DATA_PATH)

    df = pd.DataFrame(
        {
            "facility_id": ["A"],
            "row_count": [10],
            "missingness_rate": [0.1],
            "quality_score": [0.9],
        }
    )
    df.to_csv(diag.FACILITY_PATH, index=False)

    profiles = {"colX": {"null_count": 1}}  # colX not in cleaned data
    with diag.PROFILES_PATH.open("w") as f:
        json.dump(profiles, f)

    diag.SUMMARY_PATH.write_text("{}")

    with pytest.raises(ValueError):
        diag.check_consistency_with_cleaned_data()


def test_valid_consistency_passes():
    write_cleaned_data(diag.CLEANED_DATA_PATH)

    df = pd.DataFrame(
        {
            "facility_id": ["A", "B"],
            "row_count": [10, 20],
            "missingness_rate": [0.1, 0.2],
            "quality_score": [0.9, 0.8],
        }
    )
    df.to_csv(diag.FACILITY_PATH, index=False)

    profiles = {
        "col1": {"null_count": 1},
        "col2": {"null_count": 1},
    }
    with diag.PROFILES_PATH.open("w") as f:
        json.dump(profiles, f)

    diag.SUMMARY_PATH.write_text("{}")

    diag.check_consistency_with_cleaned_data()  # should not raise


# --- Deterministic behavior tests for Stage 03 intermediate artifacts ---


def test_quality_summary_is_deterministic(tmp_path, monkeypatch):
    """Repeated reads of quality_summary.json must be deterministic."""
    summary = {
        "total_rows": 3,
        "column_count": 3,
        "missingness_summary": {"col1": 1, "col2": 1},
        "quality_score": 0.95,
    }

    diag.SUMMARY_PATH.write_text(json.dumps(summary))

    s1 = json.loads(diag.SUMMARY_PATH.read_text())
    s2 = json.loads(diag.SUMMARY_PATH.read_text())

    assert s1 == s2, "quality_summary.json must be deterministic across reads"


def test_facility_metrics_is_deterministic(tmp_path, monkeypatch):
    """facility_metrics.csv must load deterministically."""
    df = pd.DataFrame(
        {
            "facility_id": ["A", "B"],
            "row_count": [10, 20],
            "missingness_rate": [0.1, 0.2],
            "quality_score": [0.9, 0.8],
        }
    )
    df.to_csv(diag.FACILITY_PATH, index=False)

    loaded1 = pd.read_csv(diag.FACILITY_PATH)
    loaded2 = pd.read_csv(diag.FACILITY_PATH)

    assert loaded1.equals(loaded2), "facility_metrics.csv must be deterministic"


def test_column_profiles_is_deterministic(tmp_path, monkeypatch):
    """column_profiles.json must load deterministically."""
    profiles = {
        "col1": {"null_count": 1, "distinct_count": 2},
        "col2": {"null_count": 1, "distinct_count": 3},
    }
    diag.PROFILES_PATH.write_text(json.dumps(profiles))

    p1 = json.loads(diag.PROFILES_PATH.read_text())
    p2 = json.loads(diag.PROFILES_PATH.read_text())

    assert p1 == p2, "column_profiles.json must be deterministic across reads"


def test_facility_metrics_column_order_is_deterministic(tmp_path, monkeypatch):
    """Column ordering in facility_metrics.csv must be deterministic."""
    df = pd.DataFrame(
        {
            "facility_id": ["A"],
            "row_count": [10],
            "missingness_rate": [0.1],
            "quality_score": [0.9],
        }
    )
    df.to_csv(diag.FACILITY_PATH, index=False)

    loaded = pd.read_csv(diag.FACILITY_PATH)
    assert list(loaded.columns) == [
        "facility_id",
        "row_count",
        "missingness_rate",
        "quality_score",
    ], "facility_metrics.csv must have deterministic column ordering"


def test_column_profiles_key_order_is_deterministic(tmp_path, monkeypatch):
    """Column profile keys must be sorted deterministically."""
    profiles = {
        "col1": {"distinct_count": 2, "null_count": 1},
    }
    diag.PROFILES_PATH.write_text(json.dumps(profiles))

    loaded = json.loads(diag.PROFILES_PATH.read_text())
    keys = list(loaded["col1"].keys())

    assert keys == sorted(
        keys
    ), "column_profiles.json keys must be sorted deterministically"


def test_consistency_check_is_deterministic(tmp_path, monkeypatch):
    """Consistency check must behave deterministically across repeated calls."""
    write_cleaned_data(diag.CLEANED_DATA_PATH)

    df = pd.DataFrame(
        {
            "facility_id": ["A", "B"],
            "row_count": [10, 20],
            "missingness_rate": [0.1, 0.2],
            "quality_score": [0.9, 0.8],
        }
    )
    df.to_csv(diag.FACILITY_PATH, index=False)

    profiles = {
        "col1": {"null_count": 1},
        "col2": {"null_count": 1},
    }
    diag.PROFILES_PATH.write_text(json.dumps(profiles))

    diag.SUMMARY_PATH.write_text("{}")

    # Should not raise — twice
    diag.check_consistency_with_cleaned_data()
    diag.check_consistency_with_cleaned_data()
