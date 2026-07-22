# Stage 04 — Reporting Layer

Generates structured reporting artifacts from Stage 03 quality metrics.

---

## Overview

Stage 04 consumes the Stage 03 intermediate artifacts and produces a complete reporting bundle containing:

- dataset‑level summary
- column‑level health assessment
- sparse column list
- facility‑level quality metrics
- top/bottom facility rankings
- a manifest (`report_index.json`) pointing to all outputs

All outputs are written to:

```text
data/stage04_processed/
```

This stage is **pure downstream**: it never mutates Stage 02 or Stage 03 data.

---

## Inputs

Stage 04 expects the following Stage 03 artifacts:

```text
data/stage03_intermediate/quality_summary.json
data/stage03_intermediate/column_profiles.json
data/stage03_intermediate/facility_metrics.csv
```

These are loaded by the runner via `load_stage03_artifacts()`.

---

## Outputs

Stage 04 writes the following artifacts:

Artifact Description
dataset_summary.json High‑level dataset completeness + quality metrics
column_health.json Per‑column completeness, dtype, distinct counts, health classification
sparse_columns.json Columns with completeness < 0.50
facility_health.csv Facility‑level completeness + quality scores
top_facilities.csv Highest‑quality facilities
bottom_facilities.csv Lowest‑quality facilities
report_index.json Manifest listing all Stage 04 outputs

All artifacts are written to:

```text
data/stage04_processed/
```

---

## Architecture

Stage 04 consists of three modules:

### 1. Report Engine

Pure functions that compute:

- dataset completeness
- column health classification
- facility quality scores
- sparse column detection

No I/O occurs in this module.

### 2. Report Formatter

Transforms raw engine outputs into JSON‑serializable structures and CSV‑ready tables.

Also pure functions — no I/O.

### 3. Report Writer

Writes all Stage 04 artifacts to disk.

This is the only module that performs filesystem operations.

---

## Runner

The orchestrator is:

```text
src/stage04_reporting/run_reporting.py
```

It performs:

1. Load Stage 03 artifacts
2. Execute report engine
3. Format results
4. Write Stage 04 artifacts
5. Log progress to `logs/runner.log`

Run manually:

```bash
python -m src.stage04_reporting.run_reporting
```

Or via Makefile:

```bash
make stage04
```

---

## Logging

Stage 04 writes logs to:

```text
logs/runner.log
```

The runner attaches a `FileHandler` so all reporting activity is captured, including:

- artifact load paths
- engine execution
- formatter execution
- writer output paths
- manifest creation

---

## Testing

All Stage 04 tests use `pytest` and `tmp_path` to ensure:

- no writes to real pipeline directories
- deterministic engine + formatter behavior
- correct artifact creation by the writer
- correct manifest generation

Run tests via:

```bash
make test
```

---

## Directory Structure

```text
src/stage04_reporting/
    __init__.py
    report_engine.py
    report_formatter.py
    report_writer.py
    run_reporting.py
    README.md   ← this file
```

---

## Notes

- Stage 04 is fully deterministic: identical Stage 03 inputs produce identical Stage 04 outputs.
- Stage 04 does not validate Stage 03 schema; it assumes Stage 03 artifacts are correct.
- Stage 04 is the final stage of Branch 1. Stage 05 (dashboards) will consume Stage 04 outputs.
