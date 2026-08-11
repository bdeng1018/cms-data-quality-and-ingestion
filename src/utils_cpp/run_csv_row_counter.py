"""
run_csv_row_counter.py
-----------------------------------------
Python wrapper for the deterministic C++ CSV row counter utility.

Purpose:
    Provide a stable Python interface for the compiled C++ utility.
    This wrapper ensures:
        - deterministic execution
        - stable exit-code propagation
        - clean integration with Python diagnostics
        - isolation of C++ details from pipeline stages

Design:
    The C++ binary emits:
        - stdout: integer row count (no prefixes, no formatting)
        - stderr: empty unless an error occurs
        - exit code: 0 on success, non-zero on failure

Usage:
    from src.utils_cpp.run_csv_row_counter import run_csv_row_counter

    result = run_csv_row_counter("path/to/file.csv")
    print(result.exit_code, result.stdout, result.stderr)
"""

import subprocess
from dataclasses import dataclass
from pathlib import Path

# ==============================================================================
# Deterministic binary resolution:
#   Resolve the C++ binary relative to THIS file, not the working directory.
#   This ensures pytest, diagnostics, and pipeline stages all behave identically.
# ==============================================================================
BINARY_PATH = Path(__file__).parent / "csv_row_counter"


@dataclass
class RowCounterResult:
    """
    Deterministic result object returned by the C++ csv_row_counter utility.

    Attributes:
        exit_code (int): Raw exit code from the C++ binary.
        stdout (str): Row count or empty string.
        stderr (str): Error message (if any).
    """

    exit_code: int
    stdout: str
    stderr: str


def run_csv_row_counter(csv_path: str) -> RowCounterResult:
    """
    Deterministic Python wrapper around the C++ csv_row_counter utility.

    Parameters:
        csv_path (str): Path to the CSV file whose rows will be counted.

    Returns:
        RowCounterResult: Structured deterministic output.

    Notes:
        - No exceptions are raised.
        - All output is stripped of whitespace.
        - Behavior matches raw C++ binary exactly.
    """

    result = subprocess.run(
        [str(BINARY_PATH), csv_path],
        capture_output=True,
        text=True,
    )

    return RowCounterResult(
        exit_code=result.returncode,
        stdout=result.stdout,
        stderr=result.stderr,
    )


def run_csv_row_counter_raw(csv_path: str) -> str:
    """
    Raw deterministic wrapper used by Stage 02 diagnostics.
    Returns ONLY the stdout emitted by the C++ binary.
    """
    result = subprocess.run(
        [str(BINARY_PATH), csv_path],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()
