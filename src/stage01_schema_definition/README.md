# Stage 01 — Schema Definition & Validation

## Overview

Stage 01 establishes the foundational schema layer for the CMS Data Quality & Ingestion pipeline.
Its purpose is to define the canonical schema, validate its structure, and ensure consistency before any ingestion or alignment logic is introduced in later stages.

This stage is intentionally self‑contained, reproducible, and fully test‑driven.

---

## Directory Structure

```text
cms-data-quality-and-ingestion/
│
├── src/
│   └── stage01_schema_definition/
│       ├── __init__.py
│       ├── schema_loader.py
│       └── schema_validator.py
│
├── scripts/
│   └── diagnostics/
│       └── stage01/
│           └── check_schema.py
│
├── tests/
│   └── stage01_schema_definition/
│       ├── test_schema_loader.py
│       └── test_schema_validator.py
│
└── Makefile
```

---

## Schema Format

Stage 01 uses a canonical JSON schema with the following top‑level structure:

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

- The top‑level key must be `fields`.
- Each field must have:
  - `name` (string)
  - `type` (one of the allowed types)
- Field names must be unique.

---

## Components

`schema_loader.py`

Loads and returns the schema JSON from disk.
Used by diagnostics, tests, and later ingestion stages.

`schema_validator.py`

Provides three core validation functions:

- `check_for_duplicate_fields(fields)`
- `check_for_missing_types(fields)`
- `check_for_invalid_types(fields)`

Also provides `validate_schema(schema)` which aggregates all validation checks.

### Diagnostics Script

`scripts/diagnostics/stage01/check_schema.py`  
Runs the loader + validator and prints human‑readable results.

Example output:

```text
Running Stage 01 — Schema Diagnostics...

✓ Schema is valid.
```

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
schema-diagnostics   → runs Stage 01 diagnostics
test                 → runs pytest suite
clean-cache          → removes Python + pytest caches
```

---

## Expected Outputs

### Diagnostics

```text
✓ Schema is valid.
```

### Tests

```text
9 passed
```

### Validator

No exceptions; returns empty error list for valid schema.

---

## Completion Criteria

Stage 01 is considered complete when:

- Schema loads successfully
- All validation functions behave correctly
- Diagnostics report a valid schema
- All tests pass
- Makefile targets run cleanly
- No import or path issues remain
