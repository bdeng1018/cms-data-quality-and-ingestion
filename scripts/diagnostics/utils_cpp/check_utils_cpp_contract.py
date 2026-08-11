"""
Diagnostics — Utils C++ Contract
Validates deterministic behavior and structural correctness of the C++ utilities
in src/utils_cpp/. Ensures the csv_row_counter binary, its wrapper, and related
metadata follow the expected deterministic contract.

Checks performed:
- Binary existence and permissions
- Deterministic binary execution
- Deterministic wrapper execution
- Wrapper matches raw C++ output
- Correct exit-code propagation
- Stable stdout/stderr across runs
"""

import os
import subprocess
from pathlib import Path

from src.utils_cpp.run_csv_row_counter import run_csv_row_counter

CSV_PATH = Path("data/stage02_cleaned/cleaned_data.csv")
BINARY_PATH = Path("src/utils_cpp/csv_row_counter")


def check_binary_exists():
    if not BINARY_PATH.exists():
        raise FileNotFoundError(f"C++ utils binary missing: {BINARY_PATH}")


def check_binary_permissions():
    """Ensure the binary is executable."""
    if not os.access(BINARY_PATH, os.X_OK):
        raise AssertionError(f"C++ binary is not executable: {BINARY_PATH}")


def run_cpp_direct():
    """Run the raw C++ binary directly."""
    result = subprocess.run(
        [str(BINARY_PATH), str(CSV_PATH)], capture_output=True, text=True
    )
    return result


def check_binary_determinism():
    """Ensure raw C++ binary produces deterministic output."""
    r1 = run_cpp_direct()
    r2 = run_cpp_direct()

    if r1.returncode != r2.returncode:
        raise AssertionError("C++ binary exit code is non-deterministic")

    if r1.stdout != r2.stdout:
        raise AssertionError("C++ binary stdout is non-deterministic")

    if r1.stderr != r2.stderr:
        raise AssertionError("C++ binary stderr is non-deterministic")


def check_wrapper_determinism():
    """Ensure wrapper produces deterministic output."""
    w1 = run_csv_row_counter(str(CSV_PATH))
    w2 = run_csv_row_counter(str(CSV_PATH))

    if w1.exit_code != w2.exit_code:
        raise AssertionError("Wrapper exit code is non-deterministic")

    if w1.stdout != w2.stdout:
        raise AssertionError("Wrapper stdout is non-deterministic")

    if w1.stderr != w2.stderr:
        raise AssertionError("Wrapper stderr is non-deterministic")


def check_wrapper_matches_cpp():
    """Ensure wrapper output matches raw C++ binary behavior."""
    cpp = run_cpp_direct()
    wrapper = run_csv_row_counter(str(CSV_PATH))

    if cpp.returncode != wrapper.exit_code:
        raise AssertionError(
            f"Exit code mismatch: cpp={cpp.returncode}, wrapper={wrapper.exit_code}"
        )

    if cpp.stdout != wrapper.stdout:
        raise AssertionError("Wrapper stdout does not match C++ stdout")

    if cpp.stderr != wrapper.stderr:
        raise AssertionError("Wrapper stderr does not match C++ stderr")


def main():
    check_binary_exists()
    check_binary_permissions()
    check_binary_determinism()
    check_wrapper_determinism()
    check_wrapper_matches_cpp()
    print("Utils C++ contract diagnostics passed.")


if __name__ == "__main__":
    main()
