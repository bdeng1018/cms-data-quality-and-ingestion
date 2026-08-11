# Stage 01 — Schema Definition, Validation & Deterministic Boundary Enforcement

## Overview

Stage 01 establishes the **canonical schema layer** for the CMS Data Quality & Ingestion Pipeline.
It defines the authoritative schema, validates its structure, and enforces deterministic boundary rules before any ingestion, cleaning, or alignment logic occurs in later stages.

This stage is intentionally:

- deterministic
- reproducible
- isolated
- contract‑driven
- fully test‑driven

It is the **first correctness gate** in the pipeline.

---

## Directory Structure

```text
cms-data-quality-and-ingestion/
│
├── src/
│   └── stage01_schema_definition/
│       ├── __init__.py
│       ├── schema_loader.py
│       ├── schema_validator.py
│       └── cpp_schema_validator.cpp     # deterministic C++ boundary validator
│
├── scripts/
│   └── diagnostics/
│       └── stage01/
│           └── check_schema.py
│
├── tests/
│   └── stage01_schema_definition/
│       ├── test_schema_loader.py
│       ├── test_schema_validator.py
│       └── test_cpp_schema_validator.py
│
└── Makefile
```

---

## Schema Format (Canonical JSON)

Stage 01 uses a strict JSON schema with the following structure:

```json
{
  "fields": [
    {
      "name": "field_name",
      "type": "string | integer | float | boolean | date | datetime"
    }
  ]
}
```

### Requirements

- Top‑level key **must** be `"fields"`.
- Each field must have:
  - `"name"` (string)
  - `"type"` (one of the allowed types)
- Field names must be **unique**.
- No additional keys are permitted unless explicitly added to the schema contract.

---

## Components

### 1. `schema_loader.py`

Loads and returns the schema JSON from disk.

Responsibilities:

- read schema file
- validate top‑level structure
- return Python dictionary
- raise deterministic exceptions on malformed input

Used by:

- diagnostics
- ingestion stages
- test suite
- provenance + manifest generation

### 2. `schema_validator.py`

Provides core validation functions:

- `check_for_duplicate_fields(fields)`
- `check_for_missing_types(fields)`
- `check_for_invalid_types(fields)`

And the aggregate validator:

- `validate_schema(schema)`

All functions are deterministic and test-driven.

### 3. Deterministic C++ Boundary Validator

`cpp_schema_validator.cpp` enforces strict ingestion‑boundary rules:

- exact column count
- exact column order
- exact column names
- deterministic single‑token outputs

Expected outputs:

- `VALID`
- `COLUMN_COUNT_MISMATCH`
- `COLUMN_NAME_MISMATCH`
- `EMPTY_CSV`

This validator is used by:

- Stage 01 diagnostics
- ingestion boundary checks
- CI/CD validation
- provenance + manifest generation

It guarantees reproducible behavior across environments.

---

## Diagnostics

`scripts/diagnostics/stage01/check_schema.py`
Runs loader + validator and prints human‑readable results.

Example:

```text
Running Stage 01 — Schema Diagnostics...

✓ Schema is valid.
```

Diagnostics are deterministic and do not mutate source data.

---

## How to Run Stage 01

### 1. Run the loader

```bash
python -m src.stage01_schema_definition.schema_loader
```

### 2. Run the validator

```bash
python -m src.stage01_schema_definition.schema_validator
```

### 3. Run diagnostics

```bash
python scripts/diagnostics/stage01/check_schema.py
```

### 4. Run tests

```bash
pytest -q
```

### 5. Run via Makefile

```bash
make schema-diagnostics
make test
make clean-cache
```

---

## Makefile Targets

```text
schema-diagnostics   → run Stage 01 diagnostics
test                 → run pytest suite
clean-cache          → remove Python + pytest caches
cpp-schema           → build deterministic C++ validator
```

---

## Expected Outputs

### Diagnostics

```text
✓ Schema is valid.
```

### Python Tests

```text
9 passed
```

### C++ Validator Tests

```text
4 passed
```

### Validator Output

For valid schema:

```code
VALID
```

For mismatches:

```code
COLUMN_COUNT_MISMATCH
COLUMN_NAME_MISMATCH
EMPTY_CSV
```

---

## Completion Criteria

Stage 01 is complete when:

- schema loads successfully
- validation functions behave deterministically
- C++ validator emits correct single‑token outputs
- diagnostics report valid schema
- all Python + C++ tests pass
- Makefile targets run cleanly
- no import or path issues remain
- schema contract is stable and reproducible
