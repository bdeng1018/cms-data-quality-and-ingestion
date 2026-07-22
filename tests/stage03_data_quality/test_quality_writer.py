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
