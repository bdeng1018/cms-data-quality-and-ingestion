"""
Diagnostics — Stage 04 Report Contract
Validates deterministic structure and content of Stage 04 reporting artifacts.
Ensures that facility-level and dataset-level reports follow the expected
contract and remain stable across runs.

Checks performed:
- Artifact existence
- Required fields in each artifact
- Non-empty facility health metrics
- Deterministic ordering
- Cross-stage consistency with Stage 03 artifacts
"""

import csv
import json
from pathlib import Path

# Stage 04 artifacts
HEALTH_PATH = Path("data/stage04_processed/facility_health_contract.csv")
SUMMARY_PATH = Path("data/stage04_processed/dataset_summary.json")
INDEX_PATH = Path("data/stage04_processed/report_index.json")

# Stage 03 artifacts (for cross-stage consistency)
METRICS_PATH = Path("data/stage03_intermediate/facility_metrics.csv")


def check_files_exist():
    missing = []
    for p in [HEALTH_PATH, SUMMARY_PATH, INDEX_PATH, METRICS_PATH]:
        if not p.exists():
            missing.append(str(p))
    if missing:
        raise FileNotFoundError(f"Missing Stage 04 artifacts: {missing}")


def load_dataset_summary():
    with open(SUMMARY_PATH) as f:
        return json.load(f)


def load_report_index():
    with open(INDEX_PATH) as f:
        return json.load(f)


def check_facility_health_contract():
    """Ensure facility_health_contract.csv has required columns and non-empty rows."""
    with open(HEALTH_PATH) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        raise AssertionError("facility_health_contract.csv is empty")

    required = {
        "facility_id",
        "quality_score",
        "health_flag",
        "missing_values",
        "warnings",
    }

    missing = required - set(rows[0].keys())
    if missing:
        raise AssertionError(f"Missing required facility health columns: {missing}")


def check_dataset_summary_contract():
    """Ensure dataset_summary.json contains required fields."""
    summary = load_dataset_summary()

    required = {
        "total_facilities",
        "total_rows",
        "overall_quality_score",
        "report_generated_at",
        "warnings",
    }

    missing = required - set(summary.keys())
    if missing:
        raise AssertionError(f"Missing dataset summary fields: {missing}")

    if not isinstance(summary["warnings"], list):
        raise AssertionError("warnings must be a list")


def check_report_index_contract():
    """Ensure report_index.json contains deterministic structure."""
    index = load_report_index()

    required = {"reports", "version"}
    missing = required - set(index.keys())
    if missing:
        raise AssertionError(f"Missing report index fields: {missing}")

    if not isinstance(index["reports"], list):
        raise AssertionError("reports must be a list")

    # Ensure deterministic ordering of report entries
    report_names = [r["name"] for r in index["reports"]]
    if report_names != sorted(report_names):
        raise AssertionError(
            "report_index.json entries must be sorted deterministically"
        )


def check_cross_stage_consistency():
    """Ensure facility IDs in Stage 04 match Stage 03 metrics."""
    # Load Stage 03 facility IDs
    with open(METRICS_PATH) as f:
        reader = csv.DictReader(f)
        stage03_ids = {row["facility_id"] for row in reader}

    # Load Stage 04 facility IDs (contract version)
    with open(HEALTH_PATH) as f:
        reader = csv.DictReader(f)
        stage04_ids = {row["facility_id"] for row in reader}

    if stage03_ids != stage04_ids:
        raise AssertionError("Facility IDs mismatch between Stage 03 and Stage 04")


def main():
    check_files_exist()
    check_facility_health_contract()
    check_dataset_summary_contract()
    check_report_index_contract()
    check_cross_stage_consistency()
    print("Stage 04 report contract diagnostics passed.")


if __name__ == "__main__":
    main()
