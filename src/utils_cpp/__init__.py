"""
utils_cpp package
-----------------------------------------
Python interface layer for deterministic C++ mechanization utilities.

Overview:
    This package provides stable, reproducible Python bindings for the small,
    single‑purpose C++ binaries used throughout the ingestion pipeline. These
    utilities support DT&E‑style reproducibility, ingestion diagnostics, and
    contract‑driven validation across pipeline stages.

Included Mechanization Utilities:
    csv_row_counter.cpp
        Deterministic row‑counting utility.
        Emits:
            stdout: integer row count (no prefixes, no formatting)
            stderr: empty on success
            exit code: 0 on success

    schema_validator.cpp
        Deterministic schema validation utility.
        Emits:
            stdout: validation result (machine‑readable)
            stderr: empty on success
            exit code: 0 on success

    ingestion_utils.cpp
        Deterministic ingestion helper functions (e.g., file checks, metadata
        extraction). Behaves consistently with the same stdout/stderr contract.

Python Wrappers:
    run_csv_row_counter.py
        Provides a deterministic Python interface to csv_row_counter.
        Ensures:
            - stable subprocess execution
            - correct exit‑code propagation
            - whitespace‑stripped stdout/stderr
            - import‑safe binary resolution

    run_schema_validator.py
        Wrapper for schema_validator with identical deterministic guarantees.

    run_ingestion_utils.py
        Wrapper for ingestion_utils with deterministic output contracts.

Design Principles:
    - All C++ utilities must produce machine‑readable stdout.
    - stderr must remain empty on success to avoid contaminating diagnostics.
    - Python wrappers must return structured, deterministic objects.
    - No wrapper may introduce formatting, prefixes, or logging noise.
    - All paths must be resolved relative to this package, not the working
      directory, to ensure stability under pytest, CI/CD, and pipeline runners.

Usage:
    from src.utils_cpp import run_csv_row_counter

    result = run_csv_row_counter("path/to/file.csv")
    print(result.exit_code, result.stdout, result.stderr)

Notes:
    This package exists to ensure that Python can import the C++ wrappers as a
    proper module, enabling deterministic behavior across all execution
    environments (pytest, diagnostics, pipeline stages, CI/CD).
"""

# Expose high‑level wrapper(s) at the package level for convenience.
from .run_csv_row_counter import RowCounterResult, run_csv_row_counter
