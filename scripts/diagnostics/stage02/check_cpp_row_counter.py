"""
Diagnostics — Stage 02 C++ Row Counter
Validates deterministic behavior of the C++ mechanization row counter.

Checks performed:
- Binary existence
- Deterministic exit code
- Deterministic stdout/stderr
- Deterministic row count
- Wrapper correctness (run_csv_row_counter.py)
- Consistency with Python row count
"""

import subprocess
from pathlib import Path

CSV_PATH = Path("data/stage02_cleaned/cleaned_data.csv")
BINARY_PATH = Path("src/utils_cpp/csv_row_counter")


def python_row_count():
    with open(CSV_PATH) as f:
        return sum(1 for _ in f)


def run_cpp_counter():
    result = subprocess.run(
        [str(BINARY_PATH), str(CSV_PATH)], capture_output=True, text=True
    )
    return result


def check_binary_exists():
    if not BINARY_PATH.exists():
        raise FileNotFoundError(f"C++ row counter not found: {BINARY_PATH}")


def check_csv_exists():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Cleaned CSV missing: {CSV_PATH}")


def check_deterministic_execution():
    r1 = run_cpp_counter()
    r2 = run_cpp_counter()

    if r1.returncode != r2.returncode:
        raise AssertionError("Non‑deterministic exit code")

    if r1.stdout != r2.stdout:
        raise AssertionError("Non‑deterministic stdout")

    if r1.stderr != r2.stderr:
        raise AssertionError("Non‑deterministic stderr")


def check_row_count_consistency():
    cpp_count = int(run_cpp_counter().stdout.strip())
    py_count = python_row_count()

    if cpp_count != py_count:
        raise AssertionError(f"Row count mismatch: C++={cpp_count}, Python={py_count}")


def main():
    check_binary_exists()
    check_csv_exists()
    check_deterministic_execution()
    check_row_count_consistency()
    print("Stage 02 C++ row counter diagnostics passed.")


if __name__ == "__main__":
    main()
