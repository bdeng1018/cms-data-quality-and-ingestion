"""
Tests for Stage 03 Quality Writer

Validates:
    - directory creation
    - JSON writing (dataset-level metrics)
    - CSV writing (facility-level metrics)
    - JSON writing (column-level profiles)
    - overwrite behavior
    - correct file contents
"""

import json

import pandas as pd
import pytest

import src.stage03_data_quality.quality_writer as writer


@pytest.fixture(autouse=True)
def patch_writer_paths(tmp_path, monkeypatch):
    """
    Redirect writer output directory to tmp_path.
    Prevents tests from touching real Stage 03 artifacts.
    """
    fake_dir = tmp_path / "stage03_intermediate"
    fake_dir.mkdir()

    # Patch new writer constant (replaces old INTERMEDIATE_DIR)
    monkeypatch.setattr(
        "src.stage03_data_quality.quality_writer.DEFAULT_INTERMEDIATE_DIR", fake_dir
    )

    return fake_dir


def test_write_quality_summary_creates_directory_and_file(patch_writer_paths):
    summary = {
        "total_rows": 100,
        "column_count": 10,
        "missingness_summary": {"col1": 5},
        "quality_score": 0.95,
    }

    writer.write_quality_summary(summary, base_dir=patch_writer_paths)

    out_path = patch_writer_paths / "quality_summary.json"
    assert out_path.exists()

    with out_path.open("r") as f:
        data = json.load(f)

    assert data["total_rows"] == 100
    assert data["quality_score"] == 0.95


def test_write_facility_metrics_writes_csv_correctly(patch_writer_paths):
    df = pd.DataFrame(
        {
            "facility_id": ["A", "B"],
            "row_count": [50, 50],
            "missingness_rate": [0.1, 0.2],
            "quality_score": [0.9, 0.8],
        }
    )

    writer.write_facility_metrics(df, base_dir=patch_writer_paths)

    out_path = patch_writer_paths / "facility_metrics.csv"
    assert out_path.exists()

    df_loaded = pd.read_csv(out_path)
    assert len(df_loaded) == 2
    assert "facility_id" in df_loaded.columns
    assert df_loaded.loc[0, "row_count"] == 50


def test_write_column_profiles_writes_json_correctly(patch_writer_paths):
    profiles = {
        "col1": {
            "null_count": 5,
            "distinct_count": 95,
            "inferred_dtype": "int64",
            "quality_score": 0.98,
        }
    }

    writer.write_column_profiles(profiles, base_dir=patch_writer_paths)

    out_path = patch_writer_paths / "column_profiles.json"
    assert out_path.exists()

    with out_path.open("r") as f:
        data = json.load(f)

    assert "col1" in data
    assert data["col1"]["null_count"] == 5
    assert data["col1"]["quality_score"] == 0.98


def test_writer_overwrites_existing_files(patch_writer_paths):
    profiles_initial = {"col1": {"null_count": 10}}
    profiles_updated = {"col1": {"null_count": 3}}

    writer.write_column_profiles(profiles_initial, base_dir=patch_writer_paths)
    writer.write_column_profiles(profiles_updated, base_dir=patch_writer_paths)

    out_path = patch_writer_paths / "column_profiles.json"
    with out_path.open("r") as f:
        data = json.load(f)

    assert data["col1"]["null_count"] == 3


# --- Deterministic behavior tests for Stage 03 Quality Writer ---


def test_quality_summary_is_written_deterministically(patch_writer_paths):
    """Repeated writes of quality_summary.json must be identical."""
    summary = {
        "total_rows": 100,
        "column_count": 10,
        "missingness_summary": {"col1": 5, "col2": 1},
        "quality_score": 0.95,
    }

    out_path = patch_writer_paths / "quality_summary.json"

    # Write twice
    writer.write_quality_summary(summary, base_dir=patch_writer_paths)
    s1 = out_path.read_text()

    writer.write_quality_summary(summary, base_dir=patch_writer_paths)
    s2 = out_path.read_text()

    assert s1 == s2, "quality_summary.json must be deterministic across repeated writes"


def test_quality_summary_key_order_is_deterministic(patch_writer_paths):
    """JSON keys must be sorted deterministically."""
    summary = {
        "quality_score": 0.95,
        "column_count": 10,
        "total_rows": 100,
        "missingness_summary": {"col1": 5},
    }

    out_path = patch_writer_paths / "quality_summary.json"
    writer.write_quality_summary(summary, base_dir=patch_writer_paths)

    loaded = json.loads(out_path.read_text())
    keys = list(loaded.keys())

    assert keys == sorted(
        keys
    ), "quality_summary.json keys must be sorted deterministically"


def test_facility_metrics_is_written_deterministically(patch_writer_paths):
    """Repeated writes of facility_metrics.csv must be identical."""
    df = pd.DataFrame(
        {
            "facility_id": ["A", "B"],
            "row_count": [50, 50],
            "missingness_rate": [0.1, 0.2],
            "quality_score": [0.9, 0.8],
        }
    )

    out_path = patch_writer_paths / "facility_metrics.csv"

    writer.write_facility_metrics(df, base_dir=patch_writer_paths)
    f1 = pd.read_csv(out_path)

    writer.write_facility_metrics(df, base_dir=patch_writer_paths)
    f2 = pd.read_csv(out_path)

    assert f1.equals(
        f2
    ), "facility_metrics.csv must be deterministic across repeated writes"


def test_facility_metrics_column_order_is_deterministic(patch_writer_paths):
    """CSV column ordering must be deterministic."""
    df = pd.DataFrame(
        {
            "facility_id": ["A"],
            "row_count": [10],
            "missingness_rate": [0.1],
            "quality_score": [0.9],
        }
    )

    out_path = patch_writer_paths / "facility_metrics.csv"
    writer.write_facility_metrics(df, base_dir=patch_writer_paths)

    loaded = pd.read_csv(out_path)
    expected_order = [
        "facility_id",
        "row_count",
        "missingness_rate",
        "quality_score",
    ]

    assert (
        list(loaded.columns) == expected_order
    ), "facility_metrics.csv must have deterministic column ordering"


def test_column_profiles_is_written_deterministically(patch_writer_paths):
    """Repeated writes of column_profiles.json must be identical."""
    profiles = {
        "col1": {
            "null_count": 5,
            "distinct_count": 95,
            "inferred_dtype": "int64",
            "quality_score": 0.98,
        }
    }

    out_path = patch_writer_paths / "column_profiles.json"

    writer.write_column_profiles(profiles, base_dir=patch_writer_paths)
    p1 = out_path.read_text()

    writer.write_column_profiles(profiles, base_dir=patch_writer_paths)
    p2 = out_path.read_text()

    assert p1 == p2, "column_profiles.json must be deterministic across repeated writes"


def test_column_profiles_key_order_is_deterministic(patch_writer_paths):
    """Column profile keys must be sorted deterministically."""
    profiles = {
        "col1": {
            "quality_score": 0.98,
            "distinct_count": 95,
            "null_count": 5,
            "inferred_dtype": "int64",
        }
    }

    out_path = patch_writer_paths / "column_profiles.json"
    writer.write_column_profiles(profiles, base_dir=patch_writer_paths)

    loaded = json.loads(out_path.read_text())
    keys = list(loaded["col1"].keys())

    assert keys == sorted(
        keys
    ), "column_profiles.json keys must be sorted deterministically"
