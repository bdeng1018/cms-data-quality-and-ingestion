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
        json.dump(
            data,
            f,
            indent=2,
            sort_keys=True,  # deterministic key ordering
        )


# ==============================================================================
# Helper: accept both suffixed and unsuffixed keys
# ==============================================================================


def _get(formatted: dict, *keys):
    """
    Accept either:
        dataset_summary_json OR dataset_summary
        column_health_json   OR column_health
        sparse_columns_json  OR sparse_columns
        facility_health_csv  OR facility_health
        top_facilities_csv   OR top_facilities
        bottom_facilities_csv OR bottom_facilities

    This makes writer compatible with:
        - Stage 04 engine/formatter (unsuffixed)
        - Stage 04 writer tests (suffixed)
    """
    for k in keys:
        if k in formatted:
            return formatted[k]
    raise KeyError(f"None of the expected keys found: {keys}")


# ==============================================================================
# Main Writer API
# ==============================================================================


def write_reports(formatted_reports: dict, base_dir: Path = DEFAULT_OUTPUT_DIR):
    """
    Writes all Stage 04 reporting artifacts.

    formatted_reports keys (either naming convention):
        - dataset_summary_json OR dataset_summary
        - column_health_json   OR column_health
        - sparse_columns_json  OR sparse_columns
        - facility_health_csv  OR facility_health
        - top_facilities_csv   OR top_facilities
        - bottom_facilities_csv OR bottom_facilities
    """

    ensure_directory(str(base_dir))

    # Paths
    dataset_summary_path = base_dir / "dataset_summary.json"
    column_health_path = base_dir / "column_health.json"
    sparse_columns_path = base_dir / "sparse_columns.json"

    # Minimal CSVs (tests)
    facility_health_path = base_dir / "facility_health.csv"
    top_facilities_path = base_dir / "top_facilities.csv"
    bottom_facilities_path = base_dir / "bottom_facilities.csv"

    # Full contract CSVs (diagnostics)
    facility_health_contract_path = base_dir / "facility_health_contract.csv"
    top_facilities_contract_path = base_dir / "top_facilities_contract.csv"
    bottom_facilities_contract_path = base_dir / "bottom_facilities_contract.csv"

    report_index_path = base_dir / "report_index.json"

    # ----------------------------------------------------------------------
    # Write JSON artifacts
    # ----------------------------------------------------------------------
    # Write dataset summary JSON (with deterministic timestamp required by contract)
    dataset_summary = _get(formatted_reports, "dataset_summary_json", "dataset_summary")
    dataset_summary["report_generated_at"] = (
        "static"  # deterministic, contract-required
    )
    write_json(dataset_summary, dataset_summary_path)

    write_json(
        _get(formatted_reports, "column_health_json", "column_health"),
        column_health_path,
    )
    write_json(
        _get(formatted_reports, "sparse_columns_json", "sparse_columns"),
        sparse_columns_path,
    )

    # ----------------------------------------------------------------------
    # Write CSV artifacts — minimal schemas for tests
    # ----------------------------------------------------------------------
    facility_health_df = _get(
        formatted_reports, "facility_health_csv", "facility_health"
    )
    facility_health_df[["facility_id", "completeness_score", "health"]].to_csv(
        facility_health_path, index=False
    )

    top_facilities_df = _get(formatted_reports, "top_facilities_csv", "top_facilities")
    top_facilities_df[["facility_id", "completeness_score"]].to_csv(
        top_facilities_path, index=False
    )

    bottom_facilities_df = _get(
        formatted_reports, "bottom_facilities_csv", "bottom_facilities"
    )
    bottom_facilities_df[["facility_id", "completeness_score"]].to_csv(
        bottom_facilities_path, index=False
    )

    # ----------------------------------------------------------------------
    # Write CSV artifacts — full schemas for diagnostics
    # ----------------------------------------------------------------------
    facility_health_df.to_csv(facility_health_contract_path, index=False)
    top_facilities_df.to_csv(top_facilities_contract_path, index=False)
    bottom_facilities_df.to_csv(bottom_facilities_contract_path, index=False)

    # ----------------------------------------------------------------------
    # Write manifest (used by Stage 05)
    # ----------------------------------------------------------------------
    reports = [
        {"name": "dataset_summary", "path": str(dataset_summary_path)},
        {"name": "column_health", "path": str(column_health_path)},
        {"name": "sparse_columns", "path": str(sparse_columns_path)},
        # Minimal CSVs
        {"name": "facility_health", "path": str(facility_health_path)},
        {"name": "top_facilities", "path": str(top_facilities_path)},
        {"name": "bottom_facilities", "path": str(bottom_facilities_path)},
        # Contract CSVs
        {
            "name": "facility_health_contract",
            "path": str(facility_health_contract_path),
        },
        {"name": "top_facilities_contract", "path": str(top_facilities_contract_path)},
        {
            "name": "bottom_facilities_contract",
            "path": str(bottom_facilities_contract_path),
        },
    ]

    # Deterministic ordering
    reports_sorted = sorted(reports, key=lambda r: r["name"])

    # Top-level keys (required by unit tests)
    report_index = {
        "dataset_summary": str(dataset_summary_path),
        "column_health": str(column_health_path),
        "sparse_columns": str(sparse_columns_path),
        "facility_health": str(facility_health_path),
        "top_facilities": str(top_facilities_path),
        "bottom_facilities": str(bottom_facilities_path),
        # Contract CSVs
        "facility_health_contract": str(facility_health_contract_path),
        "top_facilities_contract": str(top_facilities_contract_path),
        "bottom_facilities_contract": str(bottom_facilities_contract_path),
        # Deterministic metadata
        "version": "1.0",
        "generated_at": "static",  # REQUIRED BY STAGE 04 CONTRACT
        # Contract-required list format
        "reports": reports_sorted,
    }

    write_json(report_index, report_index_path)

    return report_index
