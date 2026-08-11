# Stage 02 — Raw Ingestion Layer (CMS POS & QIES)

Stage 02 is the pipeline’s raw landing and ingestion layer. Its responsibility is to load CMS POS and QIES raw files into canonical in‑memory structures, verify essential columns, emit ingestion metadata, and expose structural diagnostics for downstream stages.

Beginning in **v1.1.0**, Stage 02 also integrates the **deterministic C++ mechanization layer**, providing reproducible row‑counting and ingestion integrity checks.

Branch 1 implements only the ingestion skeleton:

- no cleaning
- no normalization
- no CCN validation
- no POS–QIES alignment
- no domain logic

These belong to later stages.

---

## Purpose

Stage 02 defines how raw data enters the pipeline:

1. Load raw POS/QIES files (CSV or Parquet)
2. Ensure the files exist and are readable
3. Return DataFrames
4. Verify minimal required columns
5. Emit ingestion logs
6. Provide structural metadata for diagnostics
7. Run deterministic C++ row‑counting (v1.1.0)
8. Record mechanization exit codes in manifest

Full schema enforcement is handled upstream in [Stage 01](ca://s?q=Explain_Stage_01_schema_validation).

---

## Directory Structure

```text
src/stage02_raw_ingestion/
├── fetch_pos_api.py
├── base_ingestion.py
├── pos_ingestion.py
├── qies_ingestion.py
├── constants.py
├── exceptions.py
└── run_ingestion.py
```

Supporting utilities:

```text
utils/
├── file_io.py
└── logging_utils.py
```

Mechanization layer:

```text
utils_cpp/
├── csv_row_counter.cpp
├── ingestion_utils.cpp
└── schema_validator.cpp   # used by Stage 01
```

---

## Ingestion Classes

### `PosIngestionSource`

Loads CMS POS raw data:

- supports CSV/Parquet
- checks minimal POS columns
- logs ingestion events
- runs deterministic C++ row counter

### `QiesIngestionSource`

Loads CMS QIES raw data:

- supports CSV/Parquet
- checks minimal QIES columns
- logs ingestion events
- runs deterministic C++ row counter

Both classes implement:

- `load_raw()`
- `validate_minimal_structure()`
- `describe()`
- `compute_row_count_cpp()` (v1.1.0)

---

## Minimal Column Requirements

Defined in `constants.py`.

### POS

```text
ccn
provider_type
address
city
state
zip
ownership
```

### QIES

```text
ccn
qm_rating
qm_score
participation_flag
```

These are the **essential** fields required for Stage 02 ingestion.

---

## Deterministic Row Counting (v1.1.0)

Stage 02 uses the C++ mechanization layer to compute row counts:

- deterministic across all environments
- newline‑safe
- memory‑efficient
- stable across macOS/Linux/Docker/K8s

Python wrapper:

```python
from utils_cpp import row_counter

rows = row_counter.count(csv_path)
```

Manifest fields added:

```json
"mechanization": {
  "row_counter_exit_code": 0
}
```

Diagnostics include:

- Python row count
- C++ row count
- mismatch detection
- mechanization exit codes

More details: [mechanization layer](ca://s?q=Explain_C%2B%2B_mechanization_layer).

---

## Exceptions

Defined in `exceptions.py`:

- `MissingRawFileError`
- `InvalidRawShapeError`

These provide predictable error signaling for ingestion failures.

Mechanization errors propagate as:

- `MechanizationError` (Python wrapper)
- non‑zero C++ exit codes
- deterministic stderr written to `logs/mechanization.log`

---

## Logging

All ingestion logs are written to:

```text
logs/ingestion.log
```

Mechanization logs:

```text
logs/mechanization.log
```

Logging format is defined in `logging_utils.py`.

---

## Local Runner

`run_ingestion.py` provides a simple manual entry point for loading raw POS or QIES files without invoking the full pipeline.

```bash
python run_ingestion.py pos data/stage02_raw/pos_q2_2026.csv
python run_ingestion.py qies /absolute/or/relative/path/to/qies_file.csv
```

This runner is intended for:

- development
- smoke testing
- debugging ingestion behavior
- verifying minimal column presence
- verifying deterministic row counts (v1.1.0)

It does **not** perform cleaning, normalization, CCN validation, or alignment.

---

## Tests

Stage 02 uses smoke tests (Branch 1):

```text
tests/stage02_raw_ingestion/
├── test_base_ingestion.py
├── test_pos_ingestion.py
└── test_qies_ingestion.py
```

Tests verify:

- module imports
- class instantiation
- DataFrame returned
- minimal columns present
- C++ row counter integration (v1.1.0)

Mechanization tests live under:

```text
tests/utils_cpp/
```

---

## Data Landing Zone

All raw ingestion outputs land in:

```text
data/stage02_raw/
```

This is the canonical raw zone for the pipeline.

---

## Relationship to Other Stages

- **Stage 01** — full schema validation + C++ schema validator
- **Stage 02** — raw ingestion + C++ row counting
- **Stage 03** — quality checks
- **Stage 04** — reporting
- **Stage 05** — pipeline orchestration

Stage 02 is the bridge between schema definition and quality.

---

## Mechanization Provenance (v1.1.0)

Stage 02 contributes mechanization metadata to the manifest:

```json
"mechanization": {
  "mode": "python+cpp",
  "row_counter_exit_code": 0
}
```

Provenance fields:

- `mechanization_mode`
- `cpp_compiler_version`

More details: [manifest spec](ca://s?q=Show_manifest_spec_mechanization_fields).
