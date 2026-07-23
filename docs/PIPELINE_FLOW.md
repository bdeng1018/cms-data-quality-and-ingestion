# Pipeline Flow — CMS Data Quality & Ingestion Pipeline

This document explains how data moves through the CMS Data Quality & Ingestion Pipeline.  
It provides a stage‑by‑stage walkthrough of the execution flow, the artifacts produced, and how each stage depends on the previous one.

---

## 1. Overview

The pipeline processes CMS POS/QIES data through five stages:

```text
Stage 01 → Stage 02 → Stage 03 → Stage 04 → Stage 05
```

Each stage is deterministic, diagnosable, and produces well‑defined artifacts.

---

## 2. End‑to‑End Flow Diagram

```text
                ┌──────────────────────────────┐
                │        Raw POS/QIES          │
                └───────────────┬──────────────┘
                                │
                                ▼
        ┌────────────────────────────────────────────────┐
        │                Stage 02 — Ingestion            │
        │  - Fetch POS                                   │
        │  - Ingest POS/QIES                             │
        │  - Clean POS                                   │
        └───────────────┬────────────────────────────────┘
                        │
                        ▼
        ┌────────────────────────────────────────────────┐
        │           Stage 02 Output (Cleaned Data)       │
        │     data/stage02_cleaned/cleaned_data.csv      │
        └───────────────┬────────────────────────────────┘
                        │
                        ▼
        ┌────────────────────────────────────────────────┐
        │         Stage 01 — Schema Definition           │
        │  - Regenerate schema.json                      │
        │  - Validate schema                             │
        └───────────────┬────────────────────────────────┘
                        │
                        ▼
        ┌────────────────────────────────────────────────┐
        │         Stage 03 — Data Quality Profiling      │
        │  - Run quality checks                          │
        │  - Generate intermediate artifacts             │
        └───────────────┬────────────────────────────────┘
                        │
                        ▼
        ┌────────────────────────────────────────────────┐
        │             Stage 04 — Reporting               │
        │  - Build reports                               │
        │  - Format outputs                              │
        └───────────────┬────────────────────────────────┘
                        │
                        ▼
        ┌────────────────────────────────────────────────┐
        │      Stage 05 — Pipeline Orchestrator          │
        │  - Execute Stages 01–04                        │
        │  - Produce pipeline summary                    │
        └────────────────────────────────────────────────┘
```

---

## 3. Stage‑by‑Stage Flow

### Stage 02 → Stage 01

Although Stage 01 appears first numerically, it depends on Stage 02:

- Stage 02 produces the canonical cleaned dataset.
- Stage 01 regenerates `schema.json` from that cleaned dataset.

This ensures the schema always reflects real data.

### Stage 01 → Stage 03

Stage 03 uses:

- the cleaned data from Stage 02
- the schema from Stage 01

Quality checks rely on schema consistency.

### Stage 03 → Stage 04

Stage 04 consumes Stage 03’s intermediate artifacts:

- metrics
- distributions
- quality flags
- summaries

These artifacts drive the reporting engine.

### Stage 04 → Stage 05

Stage 05 orchestrates:

- Stage 01
- Stage 02
- Stage 03
- Stage 04

Then writes:

```code
data/stage05_reports/pipeline_summary.json
```

This summary is the final output of the entire pipeline.

---

## 4. Artifact Flow Summary

| Stage | Input | Output |
|-------|-------|--------|
| Stage 02 | Raw POS/QIES | `stage02_raw/`, `stage02_cleaned/cleaned_data.csv` |
| Stage 01 | Cleaned data | `stage01_schema/schema.json` |
| Stage 03 | Cleaned data + schema | `stage03_intermediate/` |
| Stage 04 | Intermediate artifacts | `stage04_processed/` |
| Stage 05 | All previous outputs | `stage05_reports/pipeline_summary.json` |

---

## 5. Diagnostics Flow

Diagnostics run in parallel with the pipeline:

```code
Stage 01 → schema-diagnostics
Stage 02 → diag-pos, diag-qies, diag-cleaned
Stage 03 → diag-quality, diag-intermediate
Stage 04 → diag-stage04
Stage 05 → diag-pipeline
```

Running:

```bash
make diagnostics
```

executes all of them in order.

---

## 6. Logging Flow

Logs are stage‑specific:

```code
logs/ingestion.log        # Stage 02
logs/quality.log          # Stage 03
logs/runner.log           # Stage 04
```

Stage 05 does not create a new log file.
Instead, it produces a final summary artifact.

---

## 7. Final Output

The final deliverable of the pipeline is:

```code
data/stage05_reports/pipeline_summary.json
```

This file contains:

- stage execution order
- success/failure status
- timestamps
- total pipeline duration

It is the authoritative record of the pipeline run.

---

## 8. Contact

Maintainer: Brian Deng <br>
Email: <bdeng.data.pipelines@gmail.com> <br>
GitHub: <https://github.com/bdeng1018>
