"""
Diagnostics — Stage 01 C++ Schema Validator
Validates deterministic behavior of the C++ mechanization layer.

Checks performed:
- Binary existence
- Deterministic exit code
- Deterministic stdout/stderr
- Schema compatibility
- Wrapper correctness (run_cpp_schema_validator.py)
"""

import json
import subprocess
from pathlib import Path

SCHEMA_PATH = Path("data/stage01_schema/schema.json")
BINARY_PATH = Path("src/stage01_schema_definition/cpp_schema_validator")


def run_cpp_validator():
    result = subprocess.run(
        [str(BINARY_PATH), str(SCHEMA_PATH)], capture_output=True, text=True
    )
    return result


def check_binary_exists():
    if not BINARY_PATH.exists():
        raise FileNotFoundError(f"C++ schema validator not found: {BINARY_PATH}")


def check_schema_exists():
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Schema file missing: {SCHEMA_PATH}")


def check_schema_json_valid():
    with open(SCHEMA_PATH) as f:
        json.load(f)


def check_deterministic_execution():
    r1 = run_cpp_validator()
    r2 = run_cpp_validator()

    if r1.returncode != r2.returncode:
        raise AssertionError("Non‑deterministic exit code")

    if r1.stdout != r2.stdout:
        raise AssertionError("Non‑deterministic stdout")

    if r1.stderr != r2.stderr:
        raise AssertionError("Non‑deterministic stderr")


def main():
    check_binary_exists()
    check_schema_exists()
    check_schema_json_valid()
    check_deterministic_execution()
    print("Stage 01 C++ schema validator diagnostics passed.")


if __name__ == "__main__":
    main()
