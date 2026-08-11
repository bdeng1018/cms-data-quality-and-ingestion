"""
Diagnostics — Stage 01 C++ Schema Wrapper
Validates deterministic behavior of the Python wrapper around the C++ schema
validator. Ensures wrapper correctness, stable subprocess invocation, and
consistent exit-code propagation.

Checks performed:
- Wrapper importability
- Deterministic wrapper output
- Deterministic wrapper exit code
- Wrapper matches raw C++ validator behavior
"""

import json
import subprocess
from pathlib import Path

from src.stage01_schema_definition.run_cpp_schema_validator import (
    run_cpp_schema_validator,
)

# Stage 01 requires BOTH schema + CSV header input
SCHEMA_PATH = Path("data/stage01_schema/schema.json")
CSV_PATH = Path("data/stage01_schema/input.csv")

BINARY_PATH = Path("src/stage01_schema_definition/cpp_schema_validator")


def run_cpp_direct():
    """Run the raw C++ binary directly."""
    result = subprocess.run(
        [str(BINARY_PATH), str(SCHEMA_PATH), str(CSV_PATH)],
        capture_output=True,
        text=True,
    )
    return result


def check_schema_exists():
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Schema file missing: {SCHEMA_PATH}")

    # Validate JSON structure
    with open(SCHEMA_PATH) as f:
        json.load(f)


def check_csv_exists():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV file missing: {CSV_PATH}")


def check_binary_exists():
    if not BINARY_PATH.exists():
        raise FileNotFoundError(f"C++ schema validator not found: {BINARY_PATH}")


def check_wrapper_determinism():
    """Ensure wrapper produces deterministic results."""
    r1 = run_cpp_schema_validator(str(SCHEMA_PATH), str(CSV_PATH))
    r2 = run_cpp_schema_validator(str(SCHEMA_PATH), str(CSV_PATH))

    if r1.exit_code != r2.exit_code:
        raise AssertionError("Wrapper exit code is non-deterministic")

    if r1.stdout != r2.stdout:
        raise AssertionError("Wrapper stdout is non-deterministic")

    if r1.stderr != r2.stderr:
        raise AssertionError("Wrapper stderr is non-deterministic")


def check_wrapper_matches_cpp():
    """Ensure wrapper output matches raw C++ binary behavior."""
    cpp = run_cpp_direct()
    wrapper = run_cpp_schema_validator(str(SCHEMA_PATH), str(CSV_PATH))

    if cpp.returncode != wrapper.exit_code:
        raise AssertionError(
            f"Wrapper exit code mismatch: cpp={cpp.returncode}, wrapper={wrapper.exit_code}"
        )

    if cpp.stdout.strip() != wrapper.stdout.strip():
        raise AssertionError("Wrapper stdout does not match C++ stdout")

    if cpp.stderr.strip() != wrapper.stderr.strip():
        raise AssertionError("Wrapper stderr does not match C++ stderr")


def main():
    check_schema_exists()
    check_csv_exists()
    check_binary_exists()
    check_wrapper_determinism()
    check_wrapper_matches_cpp()
    print("Stage 01 C++ schema wrapper diagnostics passed.")


if __name__ == "__main__":
    main()
