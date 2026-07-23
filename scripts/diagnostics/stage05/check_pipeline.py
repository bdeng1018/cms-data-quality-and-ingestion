"""
Stage 05 — Diagnostics: Pipeline Consistency Checker
================================================================================

This module validates the presence and consistency of artifacts produced by
Stages 01–05 of the CMS Data Quality & Ingestion Pipeline.

It does NOT execute any pipeline stages. It only checks:

- Stage 01 schema exists
- Stage 02 cleaned data exists
- Stage 03 intermediate artifacts exist
- Stage 04 processed reports exist
- Stage 05 summary exists

This diagnostic script is intended to be run via:

    make diagnostics

It is safe, read‑only, and deterministic.
"""

import os
import sys


# ------------------------------------------------------------------------------
# Helper: check file existence
# ------------------------------------------------------------------------------
def _check_file(path):
    """Return True if file exists, False otherwise."""
    return os.path.exists(path)


# ------------------------------------------------------------------------------
# Helper: pretty print status
# ------------------------------------------------------------------------------
def _status(label, ok):
    """Print a uniform status line."""
    state = "OK" if ok else "MISSING"
    print(f"{label:<40} : {state}")


# ------------------------------------------------------------------------------
# Stage 01 checks
# ------------------------------------------------------------------------------
def check_stage01():
    """Validate Stage 01 schema artifacts."""
    schema_path = "data/stage01_schema/schema.json"
    ok = _check_file(schema_path)
    _status("Stage 01 — schema.json", ok)
    return ok


# ------------------------------------------------------------------------------
# Stage 02 checks
# ------------------------------------------------------------------------------
def check_stage02():
    """Validate Stage 02 cleaned data artifacts."""
    cleaned_path = "data/stage02_cleaned/cleaned_data.csv"
    ok = _check_file(cleaned_path)
    _status("Stage 02 — cleaned_data.csv", ok)
    return ok


# ------------------------------------------------------------------------------
# Stage 03 checks
# ------------------------------------------------------------------------------
def check_stage03():
    """Validate Stage 03 intermediate quality artifacts."""
    artifacts = [
        "data/stage03_intermediate/quality_summary.json",
    ]

    results = []
    for p in artifacts:
        ok = _check_file(p)
        _status(f"Stage 03 — {os.path.basename(p)}", ok)
        results.append(ok)

    return all(results)


# ------------------------------------------------------------------------------
# Stage 04 checks
# ------------------------------------------------------------------------------
def check_stage04():
    """Validate Stage 04 processed report artifacts."""
    artifacts = [
        "data/stage04_processed/report_index.json",
        "data/stage04_processed/facility_health.csv",
        "data/stage04_processed/dataset_summary.json",
    ]

    results = []
    for p in artifacts:
        ok = _check_file(p)
        _status(f"Stage 04 — {os.path.basename(p)}", ok)
        results.append(ok)

    return all(results)


# ------------------------------------------------------------------------------
# Stage 05 checks
# ------------------------------------------------------------------------------
def check_stage05():
    """Validate Stage 05 pipeline summary artifact."""
    summary_path = "data/stage05_reports/pipeline_summary.json"
    ok = _check_file(summary_path)
    _status("Stage 05 — pipeline_summary.json", ok)
    return ok


# ------------------------------------------------------------------------------
# Main entrypoint
# ------------------------------------------------------------------------------
def main():
    print("\nStage 05 Diagnostics — Pipeline Consistency Check")
    print(
        "================================================================================\n"
    )

    ok01 = check_stage01()
    ok02 = check_stage02()
    ok03 = check_stage03()
    ok04 = check_stage04()
    ok05 = check_stage05()

    all_ok = all([ok01, ok02, ok03, ok04, ok05])

    print(
        "\n================================================================================"
    )
    if all_ok:
        print("Pipeline diagnostics: ALL STAGES OK")
        sys.exit(0)
    else:
        print("Pipeline diagnostics: INCONSISTENCIES FOUND")
        sys.exit(1)


if __name__ == "__main__":
    main()
