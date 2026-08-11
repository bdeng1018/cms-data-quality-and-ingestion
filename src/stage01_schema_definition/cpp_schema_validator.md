# Stage 01 — Deterministic Schema Validator (C++)

## Overview

`cpp_schema_validator.cpp` is the deterministic boundary module for Stage 01 of the CMS ingestion pipeline.
It enforces strict schema contracts before any Python logic touches the data.

This validator ensures:

- exact column count
- exact column order
- required column names
- deterministic error codes
- reproducible output across environments

This module is compiled, stable, and audit‑friendly, forming the first line of defense in the ingestion pipeline.

---

## Why C++ at the Boundary

Stage 01 is the ingestion boundary.
It must be:

- deterministic
- reproducible
- stable
- governance‑aligned

C++ provides:

- compiled determinism
- predictable behavior
- no runtime dependency drift
- stable error codes
- reproducible execution

This aligns with the pipeline’s architecture principle:

> Determinism at the boundary, flexibility inside.

---

## Inputs

### 1. Schema file (`schema.txt`)

A plain text file listing required columns in order:

```text
id
facility_name
address
city
state
zip
```

### 2. CSV file (`input.csv`)

The raw CMS ingestion file.

---

## Outputs

The validator prints one of the following:

### `VALID`

Schema matches exactly.

### `INVALID:<ERROR_CODE>:<DETAILS>`

Error codes:

- `E001` — column count mismatch
- `E002` — column name mismatch
- `E003` — column order mismatch
- `E004` — unreadable or empty file

---

## Usage

Compile:

```bash
make cpp-schema
```

Run:

```bash
./cpp_schema_validator schema.txt input.csv
```

Example output:

```code
VALID
```

Or:

```code
INVALID:E002:Column name mismatch at position 2 (expected 'address', got 'addr')
```

## Python Integration

Stage 01 Python wrapper:

```python
import subprocess

def run_schema_validator(schema_path, csv_path):
    result = subprocess.run(
        ["./cpp_schema_validator", schema_path, csv_path],
        capture_output=True,
        text=True
    )
    output = result.stdout.strip()
    if output != "VALID":
        raise ValueError(f"Schema validation failed: {output}")
```

This ensures the pipeline halts deterministically on boundary violations.

## CI/CD Integration

Pytest file: `tests/stage01_schema_definition/test_cpp_schema_validator.py`

CI/CD job should:

- compile the validator
- run the tests
- fail the pipeline on any `INVALID:*` output

This ensures deterministic boundary enforcement across environments.

## Architectural Role in Branch 1

Stage 01 is the ingestion boundary.
This validator is the compiled contract enforcer.

It guarantees:

- schema correctness
- stable ingestion behavior
- reproducible boundary checks
- deterministic failure modes

This is the foundation for:

- Stage 02 raw ingestion
- Stage 03 data quality
- Stage 04 reporting
- Stage 05 pipeline runner

## Summary

`cpp_schema_validator.cpp` is the deterministic, compiled, audit‑friendly boundary module for Stage 01.
It enforces schema correctness before any Python logic executes, ensuring reproducible ingestion behavior across all environments.
This file is a core part of the platform’s maturity and systems‑level credibility.
