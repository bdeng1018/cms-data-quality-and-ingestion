"""
Diagnostics — Utils: logging_utils.py
Validates deterministic behavior of the logging_utils module. Ensures stable
log formatting, timestamp consistency, log-level propagation, and correct
handling of repeated log writes.

Checks performed:
- Module importability
- Deterministic log formatting
- Deterministic timestamp formatting
- Correct log-level propagation
- No malformed log entries
- Stable behavior across multiple writes
"""

import json
import re
from pathlib import Path

from utils.logging_utils import get_logger

TEST_DIR = Path("tmp/diagnostics_logging_utils")
LOG_FILE = TEST_DIR / "test.log"


def setup_test_dir():
    TEST_DIR.mkdir(parents=True, exist_ok=True)
    if LOG_FILE.exists():
        LOG_FILE.unlink()


def cleanup_test_dir():
    if LOG_FILE.exists():
        LOG_FILE.unlink()
    if TEST_DIR.exists():
        TEST_DIR.rmdir()


def read_log_lines():
    if not LOG_FILE.exists():
        raise AssertionError("Log file not created by logging_utils")

    with open(LOG_FILE) as f:
        return [line.strip() for line in f if line.strip()]


def check_log_format():
    """Ensure log lines follow deterministic JSON format."""
    logger = get_logger("diag_test", LOG_FILE)
    logger.info("hello world")

    lines = read_log_lines()
    if not lines:
        raise AssertionError("Log file is empty after write")

    for line in lines:
        try:
            json.loads(line)
        except json.JSONDecodeError:
            raise AssertionError(f"Malformed JSON log line: {line}")


def check_timestamp_format():
    """Ensure timestamps follow deterministic ISO-8601 format."""
    logger = get_logger("diag_test", LOG_FILE)
    logger.info("timestamp test")

    line = read_log_lines()[-1]
    entry = json.loads(line)

    ts = entry.get("timestamp")
    if not isinstance(ts, str):
        raise AssertionError("timestamp must be a string")

    iso8601 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")
    if not iso8601.match(ts):
        raise AssertionError(f"timestamp not in ISO-8601 format: {ts}")


def check_log_level_propagation():
    """Ensure log levels propagate correctly."""
    logger = get_logger("diag_test", LOG_FILE)
    logger.warning("warn test")

    entry = json.loads(read_log_lines()[-1])
    if entry.get("level") != "WARNING":
        raise AssertionError("Log level propagation failed (expected WARNING)")


def check_multiple_writes_deterministic():
    """Ensure repeated writes produce deterministic formatting."""
    logger = get_logger("diag_test", LOG_FILE)

    logger.info("first")
    first = json.loads(read_log_lines()[-1])

    logger.info("second")
    second = json.loads(read_log_lines()[-1])

    # Check required keys exist in both entries
    required = {"timestamp", "level", "message", "logger"}
    if required - set(first.keys()):
        raise AssertionError("Missing required fields in first log entry")
    if required - set(second.keys()):
        raise AssertionError("Missing required fields in second log entry")

    # Check deterministic structure (keys sorted)
    if list(first.keys()) != sorted(first.keys()):
        raise AssertionError("Log entry keys must be sorted deterministically")
    if list(second.keys()) != sorted(second.keys()):
        raise AssertionError("Log entry keys must be sorted deterministically")


def main():
    setup_test_dir()
    try:
        check_log_format()
        check_timestamp_format()
        check_log_level_propagation()
        check_multiple_writes_deterministic()
        print("Utils logging_utils diagnostics passed.")
    finally:
        cleanup_test_dir()


if __name__ == "__main__":
    main()
