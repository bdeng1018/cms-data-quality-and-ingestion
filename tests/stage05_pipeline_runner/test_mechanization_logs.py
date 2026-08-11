"""
Tests for test_mechanization_logs.py.
Ensures mechanization log structure, provenance, and ordering are correct
when the log is present. Skips gracefully in local mode when /app/logs
does not exist.
"""

import json
from pathlib import Path

import pytest

LOG_PATH = Path("/app/logs/mechanization.log")

REQUIRED_PROVENANCE = {
    "provenance",
    "pipeline",
    "mechanization",
}

REQUIRED_MECH_FIELDS = {
    "mode",
    "cpp_compiler_version",
    "stage",
    "exit_code",
}


@pytest.fixture
def ensure_log_exists():
    if not LOG_PATH.exists():
        pytest.skip(
            "Mechanization log not generated yet; skipping mechanization log tests."
        )
    if not LOG_PATH.is_file():
        pytest.skip(
            "Mechanization log path is not a file; skipping mechanization log tests."
        )


def read_lines():
    with open(LOG_PATH) as f:
        lines = [line.strip() for line in f if line.strip()]
    assert lines, "Mechanization log must not be empty"
    return lines


@pytest.mark.xfail(reason="Deferred for future CLI validation improvements.")
def test_log_is_json_lines(ensure_log_exists):
    for line in read_lines():
        try:
            json.loads(line)
        except json.JSONDecodeError:
            raise AssertionError(f"Malformed JSON log line: {line}")


def test_required_provenance_fields_present(ensure_log_exists):
    for line in read_lines():
        entry = json.loads(line)
        missing = REQUIRED_PROVENANCE - set(entry.keys())
        assert not missing, f"Missing provenance fields: {missing}"


def test_mechanization_block_structure(ensure_log_exists):
    for line in read_lines():
        entry = json.loads(line)
        mech = entry.get("mechanization", {})
        missing = REQUIRED_MECH_FIELDS - set(mech.keys())
        assert not missing, f"Missing mechanization fields: {missing}"
        assert mech["mode"] == "python+cpp", "Mechanization mode must be python+cpp"


def test_timestamp_ordering_is_deterministic(ensure_log_exists):
    timestamps = []
    for line in read_lines():
        entry = json.loads(line)
        ts = entry.get("timestamp")
        assert isinstance(ts, str), "timestamp must be a string"
        timestamps.append(ts)

    assert timestamps == sorted(
        timestamps
    ), "Mechanization logs must be sorted by timestamp deterministically"


def test_no_empty_or_malformed_lines(ensure_log_exists):
    for raw in LOG_PATH.read_text().splitlines():
        assert raw.strip(), "Log must not contain empty lines"
        try:
            json.loads(raw)
        except Exception:
            raise AssertionError(f"Malformed log line: {raw}")
