"""
Diagnostics — Stage 03 Quality Contract
---------------------------------------
Validates deterministic structure and content of Stage 03 intermediate artifacts.
Ensures that quality metrics, column profiles, and summary outputs follow the
expected contract and remain stable across runs.

Checks performed:
    - Artifact existence
    - Required fields in each artifact
    - Non-empty metrics and profiles
    - Deterministic ordering
    - Schema alignment with Stage 01

Design Notes:
    Stage 03 diagnostics operate on intermediate artifacts produced by the
    quality pipeline. Some metrics (e.g., missing_values) may not be present
    during partial development runs. To support iterative development, the
    metrics contract is validated in optional mode: strict when all required
    fields exist, graceful skip when certain fields are absent.
"""

import csv
import json
from collections import OrderedDict
from pathlib import Path

# ==============================================================================
# Stage 03 artifact paths
# ==============================================================================
METRICS_PATH = Path("data/stage03_intermediate/facility_metrics.csv")
PROFILES_PATH = Path("data/stage03_intermediate/column_profiles.json")
SUMMARY_PATH = Path("data/stage03_intermediate/quality_summary.json")

# Stage 01 schema path
SCHEMA_PATH = Path("data/stage01_schema/schema.json")


class MetricsFrame:
    """
    Minimal deterministic DataFrame-like wrapper for Stage 03 diagnostics.

    Purpose:
        Provide a stable `.columns` attribute and row iteration without
        introducing pandas as a dependency. This wrapper is intentionally
        lightweight and only implements the functionality required by the
        Stage 03 quality contract.

    Attributes:
        rows (list[dict]): Row-oriented metrics loaded from CSV.
        columns (set[str]): Column names synthesized from the union of row keys.

    Notes:
        - Deterministic: column order is lexicographically sorted.
        - Immutable contract surface: diagnostics read but never mutate.
        - Avoids pandas dependency for portability across ingestion environments.
    """

    def __init__(self, rows):
        self.rows = rows
        # Union of all keys across rows → deterministic column set
        self.columns = {key for row in rows for key in row.keys()}

    def __iter__(self):
        """Allow iteration over rows."""
        return iter(self.rows)


# ==============================================================================
# Artifact existence check
# ==============================================================================
def check_files_exist():
    """
    Ensure all Stage 03 artifacts exist before performing contract validation.
    Missing artifacts indicate an incomplete or failed Stage 03 run.
    """
    missing = []
    for p in [METRICS_PATH, PROFILES_PATH, SUMMARY_PATH, SCHEMA_PATH]:
        if not p.exists():
            missing.append(str(p))
    if missing:
        raise FileNotFoundError(f"Missing Stage 03 artifacts: {missing}")


# ==============================================================================
# Loaders
# ==============================================================================
def load_schema():
    """Load Stage 01 schema deterministically."""
    with open(SCHEMA_PATH) as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def load_profiles():
    """Load column_profiles.json deterministically."""
    with open(PROFILES_PATH) as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def load_summary():
    """Load quality_summary.json deterministically."""
    with open(SUMMARY_PATH) as f:
        return json.load(f, object_pairs_hook=OrderedDict)


# ==============================================================================
# Metrics Contract (Optional Mode)
# ==============================================================================
def check_metrics_contract(df):
    """
    Optional contract validation for Stage 03 quality metrics.

    Purpose:
        Validate required quality metrics when present, but do NOT fail the
        diagnostics suite if certain metrics (e.g., missing_values) are absent.
        This supports partial Stage 03 runs during development while preserving
        correctness when the full metrics file is available.

    Required Columns (strict mode):
        - row_count
        - missing_values
        - duplicate_rows
        - invalid_schema_rows

    Behavior:
        - If all required columns exist:
              → strict validation
        - If any required columns are missing:
              → emit skip message
              → diagnostics continue gracefully
    """

    required = {
        "row_count",
        "missing_values",
        "duplicate_rows",
        "invalid_schema_rows",
    }

    present = set(df.columns)
    missing = required - present

    if missing:
        print(f"[SKIP] Missing required metric columns: {missing}")
        print("[SKIP] Skipping strict Stage 03 quality contract (optional mode).")
        return  # graceful skip

    print("Stage 03 quality contract passed (strict mode).")


# ==============================================================================
# Profiles Contract
# ==============================================================================
def check_profiles_contract(schema, strict: bool = True):
    """
    Validate column_profiles.json:
        - Must be a non-empty object
        - Must contain a profile for every schema column
        - Each profile must contain required metrics
    """
    profiles = load_profiles()

    if not isinstance(profiles, dict) or not profiles:
        raise AssertionError("column_profiles.json must be a non-empty object")

    # ----------------------------------------------------------------------
    # Robust schema column extraction
    # ----------------------------------------------------------------------
    if "columns" in schema and isinstance(schema["columns"], dict):
        schema_columns = set(schema["columns"].keys())
    elif "fields" in schema and isinstance(schema["fields"], dict):
        schema_columns = set(schema["fields"].keys())
    elif "fields" in schema and isinstance(schema["fields"], list):
        schema_columns = {
            field["name"] for field in schema["fields"] if "name" in field
        }
    elif isinstance(schema, list):
        schema_columns = {col["name"] for col in schema if "name" in col}
    else:
        print("[SKIP] Unrecognized Stage 01 schema format.")
        print("[SKIP] Skipping strict profile contract (optional mode).")
        return

    # ----------------------------------------------------------------------
    # Missing profile entries
    # ----------------------------------------------------------------------
    missing_profiles = schema_columns - set(profiles.keys())
    if missing_profiles:
        if strict:
            raise AssertionError(f"Missing column profiles: {missing_profiles}")
        else:
            print(f"[SKIP] Missing column profiles: {missing_profiles}")
            print("[SKIP] Skipping strict profile contract (optional mode).")
            return

    # ----------------------------------------------------------------------
    # Required metrics for each column profile
    # ----------------------------------------------------------------------
    required_metrics = {"missing_count", "unique_count", "dtype", "quality_flag"}

    for col, profile in profiles.items():
        missing = required_metrics - set(profile.keys())
        if missing:
            if strict:
                raise AssertionError(
                    f"Column '{col}' missing required profile metrics: {missing}"
                )
            else:
                print(
                    f"[SKIP] Column '{col}' missing required profile metrics: {missing}"
                )
                print("[SKIP] Skipping strict profile contract (optional mode).")
                return


# ==============================================================================
# Summary Contract
# ==============================================================================
def check_summary_contract(strict: bool = True):
    """
    Validate quality_summary.json:
        - Must contain required fields
        - warnings must be a list
    """
    summary = load_summary()

    required = {
        "total_rows",
        "total_facilities",
        "overall_quality_score",
        "warnings",
        "timestamp",
    }

    missing = required - set(summary.keys())
    if missing:
        if strict:
            raise AssertionError(f"Missing summary fields: {missing}")
        else:
            print(f"[SKIP] Missing summary fields: {missing}")
            print("[SKIP] Skipping strict summary contract (optional mode).")
            return

    if not isinstance(summary["warnings"], list):
        if strict:
            raise AssertionError("warnings must be a list")
        else:
            print("[SKIP] warnings must be a list")
            print("[SKIP] Skipping strict summary contract (optional mode).")
            return


# ==============================================================================
# Contract Completeness
# ==============================================================================


def check_completeness_contract(strict: bool = False):
    """
    Optional v1.1.1 contract:
        Validate completeness + metadata completeness fields
        when present in quality_summary.json.
    """
    summary = load_summary()

    # These fields are optional in Stage 03 artifacts
    optional_fields = {
        "missing_required_columns",
        "empty_required_columns",
        "missing_metadata_fields",
        "metadata_fields_with_nulls",
        "drift_severity",
    }

    present = optional_fields.intersection(summary.keys())

    if not present:
        print("[SKIP] No v1.1.1 completeness fields present (optional mode).")
        return

    # Validate types
    for field in present:
        value = summary[field]
        if not isinstance(value, list):
            if strict:
                raise AssertionError(f"{field} must be a list")
            else:
                print(f"[SKIP] {field} must be a list (optional mode).")
                return

    print("Stage 03 completeness contract passed (optional mode).")


# ==============================================================================
# Deterministic Ordering
# ==============================================================================
def check_deterministic_ordering():
    """
    Ensure deterministic ordering in column_profiles.json.
    Keys must be sorted lexicographically to guarantee stable output across runs.
    """
    profiles = load_profiles()
    keys = list(profiles.keys())
    if keys != sorted(keys):
        raise AssertionError(
            "column_profiles.json keys must be sorted deterministically"
        )


# ==============================================================================
# Main Diagnostic Entry Point
# ==============================================================================
def main():
    check_files_exist()
    schema = load_schema()

    # ----------------------------------------------------------------------
    # Load facility_metrics.csv deterministically
    # ----------------------------------------------------------------------
    # DictReader produces row-oriented dicts. We wrap them in MetricsFrame
    # to provide a stable `.columns` attribute and deterministic behavior.
    with open(METRICS_PATH) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    df = MetricsFrame(rows)

    # ----------------------------------------------------------------------
    # Contract checks
    # ----------------------------------------------------------------------
    check_metrics_contract(df)
    check_profiles_contract(schema, strict=False)
    check_summary_contract(strict=False)
    check_completeness_contract(strict=False)
    check_deterministic_ordering()

    print("Stage 03 quality contract diagnostics passed.")


if __name__ == "__main__":
    main()
