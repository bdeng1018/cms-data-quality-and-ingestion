"""
Stage 04 Report Writer
================================================================================
Writes formatted Stage 04 reporting artifacts into data/stage04_processed/.

Inputs (from report_formatter.format_reports()):
    - dataset_summary_json (dict)
    - column_health_json (dict)
    - sparse_columns_json (dict)
    - facility_health_csv (DataFrame)
    - top_facilities_csv (DataFrame)
    - bottom_facilities_csv (DataFrame)

Design principles:
    - All file I/O lives here
    - Deterministic, testable
    - Mirrors Stage 03 writer pattern
"""

import json
from pathlib import Path

import pandas as pd

from utils.file_io import ensure_directory

# ==============================================================================
# Default output directory
# ==============================================================================
DEFAULT_OUTPUT_DIR = Path("data/stage04_processed")


# ==============================================================================
# JSON Writers
# ==============================================================================


def write_json(data: dict, path: Path):
    with path.open("w") as f:
        json.dump(data, f, indent=2)


# ==============================================================================
# CSV Writers
# ==============================================================================


def write_csv(df: pd.DataFrame, path: Path):
    df.to_csv(path, index=False)


# ==============================================================================
# Main Writer API
# ==============================================================================


def write_reports(formatted_reports: dict, base_dir: Path = DEFAULT_OUTPUT_DIR):
    """
    Writes all Stage 04 reporting artifacts.

    formatted_reports keys:
        - dataset_summary_json
        - column_health_json
        - sparse_columns_json
        - facility_health_csv
        - top_facilities_csv
        - bottom_facilities_csv
    """

    ensure_directory(str(base_dir))

    # Paths
    dataset_summary_path = base_dir / "dataset_summary.json"
    column_health_path = base_dir / "column_health.json"
    sparse_columns_path = base_dir / "sparse_columns.json"
    facility_health_path = base_dir / "facility_health.csv"
    top_facilities_path = base_dir / "top_facilities.csv"
    bottom_facilities_path = base_dir / "bottom_facilities.csv"
    report_index_path = base_dir / "report_index.json"

    # Write JSON artifacts
    write_json(formatted_reports["dataset_summary_json"], dataset_summary_path)
    write_json(formatted_reports["column_health_json"], column_health_path)
    write_json(formatted_reports["sparse_columns_json"], sparse_columns_path)

    # Write CSV artifacts
    write_csv(formatted_reports["facility_health_csv"], facility_health_path)
    write_csv(formatted_reports["top_facilities_csv"], top_facilities_path)
    write_csv(formatted_reports["bottom_facilities_csv"], bottom_facilities_path)

    # Write manifest (useful for Stage 05)
    report_index = {
        "dataset_summary": str(dataset_summary_path),
        "column_health": str(column_health_path),
        "sparse_columns": str(sparse_columns_path),
        "facility_health": str(facility_health_path),
        "top_facilities": str(top_facilities_path),
        "bottom_facilities": str(bottom_facilities_path),
    }
    write_json(report_index, report_index_path)

    return report_index
