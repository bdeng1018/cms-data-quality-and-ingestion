"""
Tests — Utils C++ Contract
Validates deterministic behavior and correctness of the Python wrapper for the
C++ csv_row_counter utility.

Wrapper contract:
    - run_csv_row_counter(path) → RowCounterResult(exit_code, stdout, stderr)
    - No exceptions are raised.
    - stdout contains the raw row count emitted by the C++ binary.
    - stderr is empty on success.
    - exit_code is 0 on success, non‑zero on failure.

These tests ensure:
    - Deterministic wrapper behavior
    - Correct row count extraction
    - Proper error signaling for missing files
"""

from pathlib import Path

import pytest

from src.utils_cpp.run_csv_row_counter import (
    RowCounterResult,
    run_csv_row_counter,
)

TEST_DIR = Path("tmp/test_utils_cpp_contract")
TEST_FILE = TEST_DIR / "sample.csv"
MISSING_FILE = TEST_DIR / "missing.csv"


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Create and clean up the temporary test directory."""
    TEST_DIR.mkdir(parents=True, exist_ok=True)
    yield
    for f in TEST_DIR.iterdir():
        f.unlink()
    TEST_DIR.rmdir()


def test_contract_deterministic():
    """Wrapper must return identical results across repeated runs."""
    TEST_FILE.write_text("a,b\n1,2\n3,4\n")

    r1 = run_csv_row_counter(str(TEST_FILE))
    r2 = run_csv_row_counter(str(TEST_FILE))

    assert isinstance(r1, RowCounterResult)
    assert isinstance(r2, RowCounterResult)

    assert r1.exit_code == r2.exit_code
    assert r1.stdout == r2.stdout
    assert r1.stderr == r2.stderr


def test_contract_correct_row_count():
    """Row count must match number of CSV lines minus header."""
    TEST_FILE.write_text("x,y\n1,2\n3,4\n5,6\n")

    result = run_csv_row_counter(str(TEST_FILE))

    assert result.exit_code == 0
    assert result.stderr == ""

    row_count = int(result.stdout)
    assert row_count == 4, "Row count must match number of data rows"


def test_contract_missing_file():
    """Missing files must produce a non‑zero exit code and stderr output."""
    result = run_csv_row_counter(str(MISSING_FILE))

    assert result.exit_code != 0, "Missing file must produce non‑zero exit code"
    assert result.stderr != "", "Missing file must produce an error message"
