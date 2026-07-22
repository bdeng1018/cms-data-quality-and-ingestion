# Stage 02 — Raw Ingestion Layer (CMS POS & QIES)

Stage 02 is the pipeline’s raw landing and ingestion layer. Its responsibility is to load CMS POS and QIES raw files into canonical in‑memory structures, verify essential columns, and expose ingestion metadata for downstream diagnostics.

Branch 1 implements only the ingestion skeleton:

- no cleaning
- no normalization
- no CCN validation
- no POS–QIES alignment
- no domain logic

These belong to later stages.

---

## Purpose

Stage 02 defines how raw data enters the pipeline:

1. Load raw POS/QIES files (CSV or Parquet)
2. Ensure the files exist and is readable
3. Return DataFrames
4. Verify minimal required columns
5. Emit ingestion logs
6. Provide structural metadata for diagnostics and the pipeline runner

Full schema enforcement is handled upstream in Stage 01.

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

---

## Ingestion Classes

### `PosIngestionSource`

Loads CMS POS raw data:

- supports CSV/Parquet
- checks minimal POS columns
- logs ingestion events

### `QiesIngestionSource`

Loads CMS QIES raw data:

- supports CSV/Parquet
- checks minimal QIES columns
- logs ingestion events

Both classes implement:

- `load_raw()`
- `validate_minimal_structure()`
- `describe()`

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

These are the **essential** fields required for Stage 02 ingestion.

---

## Exceptions

Defined in `exceptions.py`:

- `MissingRawFileError`
- `InvalidRawShapeError`

These provide predictable error signaling for ingestion failures.

---

## Logging

All ingestion logs are written to:

```text
logs/ingestion.log
```

Logging format is defined in `logging_utils.py`.

---

## Local Runner

`run_ingestion.py` provides a simple manual entry point for loading raw POS or QIES files without invoking the full pipeline. It accepts two arguments:

1. the ingestion source (pos or qies)
2. the path to the raw CSV or Parquet file

```bash
python run_ingestion.py pos data/stage02_raw/pos_q2_2026.csv
python run_ingestion.py qies /absolute/or/relative/path/to/qies_file.csv
```

You may pass either:

- a **relative path** (recommended inside the repo)
- an **absolute path** (useful for external QIES files)

Examples:

```bash
# POS example (relative path)
python run_ingestion.py pos data/stage02_raw/pos_q2_2026.parquet

# QIES example (absolute path)
python run_ingestion.py qies /Users/<username>/downloads/qies_raw.csv
```

This runner is intended for:

- development
- smoke testing
- debugging ingestion behavior
- verifying minimal column presence

It does **not** perform cleaning, normalization, CCN validation, or alignment.

---

## Tests

Stage 02 uses **smoke tests only** (Branch 1):

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

No domain logic is tested.

---

## Data Landing Zone

All raw ingestion outputs land in:

```text
data/stage02_raw/
```

This is the canonical raw zone for the pipeline.

---

## Relationship to Other Stages

- **Stage 01** defines full schemas.
- **Stage 02** loads raw data and enforces minimal shape.
- **Stage 03** performs quality checks.
- **Stage 04** generates reports.
- **Stage 05** orchestrates the pipeline.

Stage 02 is the bridge between schema definition and quality.
