"""
Diagnostics — Stage 05 Mechanization Provenance
Validates deterministic mechanization metadata inside pipeline_summary.json.
Ensures that mechanization provenance fields exist, match expected values, and
remain stable across runs.

Checks performed:
- pipeline_summary.json existence
- mechanization block existence
- required mechanization fields
- deterministic exit codes
- correct mechanization mode
- compiler version presence
"""

import json
from pathlib import Path

SUMMARY_PATH = Path("data/stage05_reports/pipeline_summary.json")

REQUIRED_FIELDS = {
    "mode",
    "schema_validator_exit_code",
    "row_counter_exit_code",
    "cpp_compiler_version",
}


def check_summary_exists():
    if not SUMMARY_PATH.exists():
        raise FileNotFoundError(f"Pipeline summary missing: {SUMMARY_PATH}")


def load_summary():
    with open(SUMMARY_PATH) as f:
        return json.load(f)


def check_mechanization_block(summary):
    if "mechanization" not in summary:
        raise AssertionError("Missing 'mechanization' block in pipeline summary")

    mech = summary["mechanization"]

    missing = REQUIRED_FIELDS - set(mech.keys())
    if missing:
        raise AssertionError(f"Missing mechanization fields: {missing}")

    return mech


def check_mode(mech):
    if mech["mode"] != "python+cpp":
        raise AssertionError("Mechanization mode must be 'python+cpp'")


def check_exit_codes(mech):
    if not isinstance(mech["schema_validator_exit_code"], int):
        raise AssertionError("schema_validator_exit_code must be an integer")

    if not isinstance(mech["row_counter_exit_code"], int):
        raise AssertionError("row_counter_exit_code must be an integer")

    # Deterministic expectation: both should be 0 for successful runs
    if mech["schema_validator_exit_code"] != 0:
        raise AssertionError(
            f"Schema validator exit code is non-zero: {mech['schema_validator_exit_code']}"
        )

    if mech["row_counter_exit_code"] != 0:
        raise AssertionError(
            f"Row counter exit code is non-zero: {mech['row_counter_exit_code']}"
        )


def check_compiler_version(mech):
    version = mech["cpp_compiler_version"]
    if not isinstance(version, str) or not version.startswith("g++"):
        raise AssertionError(f"Invalid compiler version format: {version}")


def main():
    check_summary_exists()
    summary = load_summary()
    mech = check_mechanization_block(summary)
    check_mode(mech)
    check_exit_codes(mech)
    check_compiler_version(mech)
    print("Stage 05 mechanization provenance diagnostics passed.")


if __name__ == "__main__":
    main()
