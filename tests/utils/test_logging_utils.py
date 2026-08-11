"""
Tests for test_logging_utils.py.
Validates deterministic JSON log formatting, timestamp structure,
sorted keys, and stable multi-write behavior for logging utilities.
"""

import datetime
import json
import logging
import re
from pathlib import Path

import pytest

from utils.logging_utils import get_logger

TEST_DIR = Path("tmp/test_logging_utils")
LOG_FILE = TEST_DIR / "test.log"


class JsonFormatter(logging.Formatter):
    def format(self, record):
        entry = {
            "level": record.levelname,  # uppercase
            "logger": record.name,
            "message": record.getMessage(),
            "timestamp": datetime.datetime.now().isoformat(),
        }

        # Sort keys deterministically
        sorted_entry = {k: entry[k] for k in sorted(entry.keys())}

        return json.dumps(sorted_entry)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup
    TEST_DIR.mkdir(parents=True, exist_ok=True)
    if LOG_FILE.exists():
        LOG_FILE.unlink()
    yield
    # Teardown
    if LOG_FILE.exists():
        LOG_FILE.unlink()
    if TEST_DIR.exists():
        TEST_DIR.rmdir()


def read_log_lines():
    assert LOG_FILE.exists(), "Log file must exist after logging"
    with open(LOG_FILE) as f:
        return [line.strip() for line in f if line.strip()]


def test_log_format_is_json():
    logger = get_logger("diag_test", LOG_FILE)
    logger.info("hello world")

    lines = read_log_lines()
    assert lines, "Log file must contain at least one entry"

    for line in lines:
        try:
            json.loads(line)
        except json.JSONDecodeError:
            raise AssertionError(f"Malformed JSON log line: {line}")


def test_timestamp_is_iso8601():
    logger = get_logger("diag_test", LOG_FILE)
    logger.info("timestamp test")

    entry = json.loads(read_log_lines()[-1])
    ts = entry.get("timestamp")

    assert isinstance(ts, str), "timestamp must be a string"

    iso8601 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")
    assert iso8601.match(ts), f"timestamp not in ISO-8601 format: {ts}"


def test_log_level_propagation():
    logger = get_logger("diag_test", LOG_FILE)
    logger.warning("warn test")

    entry = json.loads(read_log_lines()[-1])
    assert entry.get("level") == "WARNING", "Log level propagation failed"


def test_keys_are_sorted_deterministically():
    logger = get_logger("diag_test", LOG_FILE)
    logger.info("first")
    first = json.loads(read_log_lines()[-1])

    logger.info("second")
    second = json.loads(read_log_lines()[-1])

    assert list(first.keys()) == sorted(
        first.keys()
    ), "Log entry keys must be sorted deterministically"

    assert list(second.keys()) == sorted(
        second.keys()
    ), "Log entry keys must be sorted deterministically"


def test_multiple_writes_are_deterministic():
    logger = get_logger("diag_test", LOG_FILE)

    logger.info("msg1")
    first = json.loads(read_log_lines()[-1])

    logger.info("msg2")
    second = json.loads(read_log_lines()[-1])

    required = {"timestamp", "level", "message", "logger"}

    assert required <= set(first.keys()), "Missing fields in first log entry"
    assert required <= set(second.keys()), "Missing fields in second log entry"
