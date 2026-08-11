"""
Tests for test_mechanization_provenance.py.
Validates the mechanization block inside pipeline_summary.json when present.
Skips gracefully in local mode when Stage 05 reports are not generated.
"""

import json
from pathlib import Path

import pytest

SUMMARY_PATH = Path("data/stage05_reports/pipeline_summary.json")

REQUIRED_FIELDS = {
    "mode",
    "schema_validator_exit_code",
    "row_counter_exit_code",
    "cpp_compiler_version",
}


@pytest.fixture
def ensure_summary_exists():
    assert SUMMARY_PATH.exists(), "pipeline_summary.json must exist"
    assert SUMMARY_PATH.is_file(), "pipeline_summary.json must be a file"


def load_summary():
    with open(SUMMARY_PATH) as f:
        return json.load(f)


def test_mechanization_block_exists(ensure_summary_exists):
    summary = load_summary()
    assert (
        "mechanization" in summary
    ), "pipeline_summary.json must contain a 'mechanization' block"


def test_required_fields_present(ensure_summary_exists):
    summary = load_summary()
    mech = summary["mechanization"]

    missing = REQUIRED_FIELDS - set(mech.keys())
    assert not missing, f"Missing mechanization fields: {missing}"


def test_mode_is_python_cpp(ensure_summary_exists):
    summary = load_summary()
    mech = summary["mechanization"]

    assert mech["mode"] == "python+cpp", "Mechanization mode must be 'python+cpp'"


def test_exit_codes_are_zero(ensure_summary_exists):
    summary = load_summary()
    mech = summary["mechanization"]

    assert isinstance(
        mech["schema_validator_exit_code"], int
    ), "schema_validator_exit_code must be an integer"
    assert isinstance(
        mech["row_counter_exit_code"], int
    ), "row_counter_exit_code must be an integer"

    assert (
        mech["schema_validator_exit_code"] == 0
    ), "schema_validator_exit_code must be 0 for successful runs"
    assert (
        mech["row_counter_exit_code"] == 0
    ), "row_counter_exit_code must be 0 for successful runs"


def test_compiler_version_format(ensure_summary_exists):
    summary = load_summary()
    mech = summary["mechanization"]

    version = mech["cpp_compiler_version"]
    assert isinstance(version, str), "cpp_compiler_version must be a string"
    assert version.startswith("g++"), "cpp_compiler_version must start with 'g++'"


def test_mechanization_block_is_deterministic(ensure_summary_exists):
    """Ensure mechanization block is stable across repeated reads."""
    s1 = load_summary()["mechanization"]
    s2 = load_summary()["mechanization"]

    assert s1 == s2, "Mechanization block must be deterministic across reads"
