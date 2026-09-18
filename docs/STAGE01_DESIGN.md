# Stage 01 Design — Deterministic Schema Definition

Stage 01 is the **ingestion boundary** of the CMS Data Quality & Ingestion Pipeline.
It is responsible for defining, validating, and enforcing the schema contract that governs all downstream stages.

This document describes the design, responsibilities, execution model, and deterministic boundary strategy of Stage 01.

---

## 1. Purpose of Stage 01

Stage 01 provides:

- Deterministic schema enforcement
- Compiled boundary validation (C++)
- Python‑level schema loading and normalization
- Cross‑language consistency checks
- Guaranteed correctness before ingestion

Unlike Stages 02–04, which operate on data, Stage 01 operates on the contract that defines the data.

Stage 01 ensures:

“No ingestion without schema validation.”

---

## 2. Inputs and Outputs

### Inputs

Stage 01 consumes:

- Schema definition file
- Raw CSV header from Stage 02
- Optional schema artifacts from diagnostics

### Outputs

Stage 01 produces:

```code
data/stage01_schema/schema.json
```

This artifact includes:

- required columns
- column order
- column count
- normalized field names
- deterministic metadata

This schema is consumed by Stages 02–04.

---

## 3. Deterministic Boundary Model

Stage 01 uses a **dual‑layer validation model**:

### Layer 1 — C++ Deterministic Validator

File:
`src/stage01_schema_definition/cpp_schema_validator.cpp`

Responsibilities:

- enforce exact column order
- enforce exact column count
- enforce exact column names
- produce deterministic error codes
- operate without Python dependencies
- behave identically across environments

This layer is the **compiled boundary**.

### Layer 2 — Python Schema Logic

Files:

- `schema_loader.py`
- `schema_validator.py`
- `run_cpp_schema_validator.py`

Responsibilities:

- load schema definitions
- normalize whitespace
- validate schema structure
- integrate C++ validator
- produce Python exceptions for CI/CD

This layer is the **integration boundary**.

Together, these layers guarantee reproducible schema enforcement.

---

## 4. Execution Model

Stage 01 executes in the following order:

```text
Load schema
↓
Normalize schema
↓
Validate schema (Python)
↓
Validate schema (C++)
↓
Write schema.json
```

Each step must succeed before the next begins.

---

## 5. C++ Validator Design

The C++ validator is intentionally minimal and deterministic.

### Why C++?

- compiled determinism
- stable error codes
- reproducible behavior
- no dependency drift
- audit‑friendly output

### Error Codes

```code
E001 — column count mismatch
E002 — column name mismatch
E003 — column order mismatch
E004 — unreadable or empty file
```

These codes are consumed by Python and CI/CD.

---

## 6. Python Integration Layer

The Python wrapper:

```python
validate_schema(schema_path, csv_path)
```

Provides:

- stable error propagation
- cross‑language integration
- deterministic failure modes
- isolation of C++ details from downstream stages

This ensures Stage 02 never calls C++ directly.

---

## 7. Schema Artifact Design

Stage 01 produces:

```code
data/stage01_schema/schema.json
```

Recommended structure:

```json
{
  "columns": [
    "id",
    "facility_name",
    "address",
    "city",
    "state",
    "zip"
  ],
  "count": 6,
  "generated_at": "2026-07-22T17:54:00",
  "source": "cpp_schema_validator"
}
```

This artifact is the authoritative schema for the pipeline.

---

## 8. CI/CD Enforcement

Stage 01 is validated through:

- `test_cpp_schema_validator.py`
- `test_schema_loader.py`
- `test_schema_validator.py`

CI/CD guarantees:

- deterministic boundary behavior
- cross‑language consistency
- reproducible schema enforcement
- stable failure modes

Stage 01 must pass all tests before Stage 02 runs.

---

## 9. Diagnostics Integration

Diagnostics for Stage 01 live under:

```code
scripts/diagnostics/stage01/
```

Tools include:

- `check_schema.py`
- `generate_schema.py`

These validate:

- schema correctness
- presence of schema.json
- consistency with Stage 02 cleaned data
- alignment with Stage 03 quality checks

Diagnostics do not run automatically; they are invoked via:

```bash
make diagnostics
```

---

## 10. Extensibility

Stage 01 supports:

- additional schema formats
- multiple ingestion sources
- future schema versions
- schema diffs
- schema evolution tracking

Adding a new schema version requires:

1. Updating `schema_loader.py`
2. Updating `schema_validator.py`
3. Adding a new C++ validator mode (optional)
4. Updating diagnostics
5. Updating CI/CD tests

The deterministic boundary model remains unchanged.

---

## 11. Contact

Maintainer: Brian Deng  <br>
Email: <bdeng.data.pipelines@gmail.com>  <br>
GitHub: <https://github.com/bdeng1018>
