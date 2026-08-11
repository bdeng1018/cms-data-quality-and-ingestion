"""
run_cpp_schema_validator.py
-----------------------------------------
Stage 01 Python wrapper for the deterministic C++ schema validator.

Purpose:
    Provide a stable Python interface for the compiled boundary module.
    This wrapper ensures:
        - deterministic execution
        - stable exit-code propagation
        - clean integration with Stage 01
        - isolation of C++ details from later stages

Design:
    The C++ validator emits exactly one uppercase token:
        VALID
        COLUMN_COUNT_MISMATCH
        COLUMN_NAME_MISMATCH
        EMPTY_CSV

    Exit codes:
        0  -> VALID
        1  -> any error condition

    This wrapper does NOT raise exceptions. Instead, it returns a structured
    result object so diagnostics and ingestion can compare raw C++ behavior
    deterministically.

Usage:
    from src.stage01_schema_definition.run_cpp_schema_validator import (
        run_cpp_schema_validator,
    )

    result = run_cpp_schema_validator("schema.json", "input.csv")
    print(result.exit_code, result.stdout, result.stderr)
"""

import subprocess
from dataclasses import dataclass
from pathlib import Path

# Path to the compiled C++ binary
BINARY_PATH = Path("src/stage01_schema_definition/cpp_schema_validator")


@dataclass
class SchemaValidatorResult:
    """
    Deterministic result object returned by the Stage 01 C++ schema validator.

    Attributes:
        exit_code (int): Raw exit code from the C++ binary.
        stdout (str): Single-token validator output (VALID or error token).
        stderr (str): Deterministic error token (if emitted on stderr).
    """

    exit_code: int
    stdout: str
    stderr: str


def run_cpp_schema_validator(schema_path: str, csv_path: str) -> SchemaValidatorResult:
    """
    Deterministic Python wrapper around the Stage 01 C++ schema validator.

    Parameters:
        schema_path (str): Path to schema definition file.
        csv_path (str): Path to CSV file whose header will be validated.

    Returns:
        SchemaValidatorResult: Structured deterministic output.

    Notes:
        - No exceptions are raised.
        - All output is stripped of whitespace.
        - Behavior matches raw C++ validator exactly.
    """

    result = subprocess.run(
        [str(BINARY_PATH), schema_path, csv_path],
        capture_output=True,
        text=True,
    )

    return SchemaValidatorResult(
        exit_code=result.returncode,
        stdout=result.stdout.strip(),
        stderr=result.stderr.strip(),
    )
