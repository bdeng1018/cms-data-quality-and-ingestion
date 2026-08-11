"""
Diagnostics — Stage 02 C++ Row Counter Wrapper
Validates deterministic behavior of the Python wrapper around the C++ row
counter. Ensures wrapper correctness, stable subprocess invocation, and
consistent exit‑code propagation.

Checks performed:
- Wrapper importability
- Deterministic wrapper output
- Deterministic wrapper exit code
- Wrapper matches raw C++ row counter behavior
- Wrapper row count matches Python row count
"""

import subprocess
from pathlib import Path

from src.utils_cpp.run_csv_row_counter import (
    run_csv_row_counter,
)

CSV_PATH = Path("data/stage02_cleaned/cleaned_data.csv")
BINARY_PATH = Path("src/utils_cpp/csv_row_counter")


def python_row_count():
    """Count rows using Python for cross‑validation."""
    with open(CSV_PATH) as f:
        return sum(1 for _ in f)


def run_cpp_direct():
    """Run the raw C++ row counter binary directly."""
    result = subprocess.run(
        [str(BINARY_PATH), str(CSV_PATH)], capture_output=True, text=True
    )
    return result


def check_csv_exists():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Cleaned CSV missing: {CSV_PATH}")


def check_binary_exists():
    if not BINARY_PATH.exists():
        raise FileNotFoundError(f"C++ row counter not found: {BINARY_PATH}")


def check_wrapper_determinism():
    """Ensure wrapper produces deterministic results."""
    r1 = run_csv_row_counter(str(CSV_PATH))
    r2 = run_csv_row_counter(str(CSV_PATH))

    if r1.exit_code != r2.exit_code:
        raise AssertionError("Wrapper exit code is non‑deterministic")

    if r1.stdout != r2.stdout:
        raise AssertionError("Wrapper stdout is non‑deterministic")

    if r1.stderr != r2.stderr:
        raise AssertionError("Wrapper stderr is non‑deterministic")


def check_wrapper_matches_cpp():
    """Ensure wrapper output matches raw C++ binary behavior."""
    cpp = run_cpp_direct()
    wrapper = run_csv_row_counter(str(CSV_PATH))

    if cpp.returncode != wrapper.exit_code:
        raise AssertionError(
            f"Wrapper exit code mismatch: cpp={cpp.returncode}, wrapper={wrapper.exit_code}"
        )

    if cpp.stdout != wrapper.stdout:
        raise AssertionError("Wrapper stdout does not match C++ stdout")

    if cpp.stderr != wrapper.stderr:
        raise AssertionError("Wrapper stderr does not match C++ stderr")


def check_row_count_consistency():
    """Ensure wrapper row count matches Python row count."""
    wrapper_count = int(run_csv_row_counter(str(CSV_PATH)).stdout.strip())
    py_count = python_row_count()

    if wrapper_count != py_count:
        raise AssertionError(
            f"Row count mismatch: wrapper={wrapper_count}, python={py_count}"
        )


def main():
    check_csv_exists()
    check_binary_exists()
    check_wrapper_determinism()
    check_wrapper_matches_cpp()
    check_row_count_consistency()
    print("Stage 02 C++ row counter wrapper diagnostics passed.")


if __name__ == "__main__":
    main()
