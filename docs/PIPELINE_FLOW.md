# Pipeline Flow — CMS Data Quality & Ingestion Pipeline (v1.1.1)

The CMS Data Quality & Ingestion Pipeline processes POS/QIES data through a deterministic, contract‑driven, five‑stage architecture.
Each stage produces well‑defined artifacts, exposes diagnostics, and feeds the next stage in a reproducible manner.

---

## 1. Overview

The pipeline executes in the following order:

```text
Stage 02 → Stage 01 → Stage 03 → Stage 04 → Stage 05
```

This ordering ensures:

- Stage 02 ingests and canonicalizes raw POS/QIES data
- Stage 01 regenerates and validates the schema from cleaned data
- Stage 03 computes deterministic quality metrics
- Stage 04 generates structured reporting artifacts
- Stage 05 orchestrates, validates, and summarizes the full run

Mechanization (C++ schema validator + C++ row counter) runs in Stages 01 and 02.

More details: [mechanization layer](ca://s?q=Explain_C%2B%2B_mechanization_layer).

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
        │  - Deterministic C++ row counting              │
        │  - Produce cleaned_data.csv                    │
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
        │  - Validate schema (Python + C++)              │
        └───────────────┬────────────────────────────────┘
                        │
                        ▼
        ┌────────────────────────────────────────────────┐
        │         Stage 03 — Data Quality Profiling      │
        │  - Run quality checks                          │
        │  - Compute completeness invariants (v1.1.1)    │
        │  - Compute metadata completeness (v1.1.1)      │
        │  - Compute drift severity (v1.1.1)             │
        │  - Generate deterministic artifacts            │
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
        │  - Collect mechanization metadata              │
        │  - Produce pipeline summary                    │
        └────────────────────────────────────────────────┘
```

---

## 3. Stage‑by‑Stage Flow

### Stage 02 → Stage 01

Stage 02 produces the canonical cleaned dataset:

```code
data/stage02_cleaned/cleaned_data.csv
```

Stage 01 uses this dataset to:

- regenerate `schema.json`
- validate schema deterministically (Python + C++)

This ensures the schema reflects real data rather than assumptions.

### Stage 01 → Stage 03

Stage 03 consumes:

- Stage 02 cleaned data
- Stage 01 schema

Quality profiling depends on schema correctness and column determinism.

### Stage 03 → Stage 04

Stage 04 consumes Stage 03’s intermediate artifacts:

- facility metrics
- column profiles
- quality summary

New v1.1.1 fields:

- `missing_required_columns`
- `empty_required_columns`
- `missing_metadata_fields`
- `metadata_fields_with_nulls`
- `drift_severity`

These invariants improve downstream reporting accuracy and schema drift visibility.

### Stage 04 → Stage 05

Stage 05 orchestrates:

- Stage 02 ingestion
- Stage 01 schema definition + validation
- Stage 03 quality profiling
- Stage 04 reporting

Then writes the final pipeline summary:

```code
data/stage05_reports/pipeline_summary.json
```

This is the authoritative record of the pipeline run.

---

## 4. Artifact Flow Summary

| Stage | Input | Output |
| ------- | ------- | -------- |
| Stage 02 | Raw POS/QIES | `stage02_raw/`, `stage02_cleaned/cleaned_data.csv` |
| Stage 01 | Cleaned data | `stage01_schema/schema.json` |
| Stage 03 | Cleaned data + schema | `stage03_intermediate/` |
| Stage 04 | Intermediate artifacts | `stage04_processed/` |
| Stage 05 | All previous outputs | `stage05_reports/pipeline_summary.json` |

All artifacts are deterministic and reproducible across environments.

---

## 5. Mechanization Flow (v1.1.1)

Mechanization runs in:

- Stage 01 → C++ schema validator
- Stage 02 → C++ row counter

Mechanization metadata is included in the final summary:

```json
"mechanization": {
  "mode": "python+cpp",
  "schema_validator_exit_code": 0,
  "row_counter_exit_code": 0,
  "cpp_compiler_version": "g++ (placeholder)"
}
```

More details: [mechanization provenance](ca://s?q=Explain_mechanization_provenance).

---

## 6. Diagnostics Flow

Diagnostics run in parallel:

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

executes all diagnostics in order.

---

## 7. Logging Flow

Logs are stage‑specific:

```code
logs/run_ingestion.log     # Stage 02
logs/schema_loader.log     # Stage 01
logs/quality.log           # Stage 03
logs/runner.log            # Stage 04
logs/mechanization.log     # Stages 01–02
```

Stage 05 produces a final summary artifact instead of a log.

---

## 8. Final Output

The final deliverable of the pipeline is:

```code
data/stage05_reports/pipeline_summary.json
```

This file contains:

- stage execution order
- success/failure status
- timestamps
- total pipeline duration
- deterministic artifact index
- mechanization metadata

It is the authoritative record of the pipeline run.

---

## 8. Contact

Maintainer: Brian Deng <br>
Email: <bdeng.data.pipelines@gmail.com> <br>
GitHub: <https://github.com/bdeng1018>
