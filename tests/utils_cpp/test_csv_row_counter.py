"""
test_csv_row_counter.py
-----------------------------------------
Deterministic tests for the C++ CSV row counter utility.

This test suite ensures:
    - stable, reproducible row counts
    - correct handling of empty files
    - correct handling of single-row files
    - correct handling of large files
    - clean Python subprocess integration

Contract of the C++ binary:
    - stdout contains ONLY the integer row count (no prefix, no formatting)
    - stderr is empty on success
    - exit code is 0 on success, non-zero on failure

This mirrors the deterministic pattern used in Stage 01 C++ validator tests.
"""

import subprocess
import tempfile
from pathlib import Path

# The C++ binary is built into the same directory as this test file
BINARY = Path(__file__).parent / "csv_row_counter"


def run_row_counter(csv_text: str):
    """
    Write CSV text to a temporary file and run the C++ row counter.

    Returns:
        (stdout, stderr) — both stripped of whitespace.
    """
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    tmp.write(csv_text.encode("utf-8"))
    tmp.close()

    result = subprocess.run(
        [str(BINARY), tmp.name],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip(), result.stderr.strip()


def test_counts_rows_correctly():
    """Basic multi-row CSV should return correct row count."""
    csv = "a,b,c\n1,2,3\n4,5,6\n"
    stdout, stderr = run_row_counter(csv)

    assert stdout == "3", "Row counter must return raw integer count"
    assert stderr == ""


def test_empty_file():
    """Empty CSV should return 0 rows."""
    stdout, stderr = run_row_counter("")
    assert stdout == "0"
    assert stderr == ""


def test_single_row():
    """CSV with only a header should return 1 row."""
    stdout, stderr = run_row_counter("a,b,c\n")
    assert stdout == "1"
    assert stderr == ""


def test_large_file():
    """Large CSV should return correct row count."""
    # 10,000 rows (1 header + 9,999 data rows)
    csv = "a,b,c\n" + "\n".join("1,2,3" for _ in range(9999))
    stdout, stderr = run_row_counter(csv)

    assert stdout == "10000"
    assert stderr == ""
