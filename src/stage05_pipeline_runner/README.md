# Stage 05 — Pipeline Runner & Summary Generator

Stage 05 provides the deterministic orchestration layer for the CMS POS/QIES
ingestion and data‑quality pipeline. It coordinates Stages 01–04, validates
required artifacts, integrates mechanization metadata, and produces the final
pipeline summary (`pipeline_summary.json`).

Stage 05 marks the completion of the deterministic pipeline in Branch 1.
Stage 06 will introduce AI/RAG/agentic augmentation on top of these outputs.

---

## Overview

Stage 05 is responsible for:

- running Stages 01–04 in fixed, deterministic order
- validating Stage 04 reporting artifacts
- collecting mechanization metadata (schema + row counter exit codes)
- producing a consolidated pipeline summary
- emitting warnings for missing or inconsistent artifacts
- enforcing deterministic subprocess execution
- integrating with Makefile targets for reproducible runs

Stage 05 **does not modify data**. It verifies, orchestrates, and summarizes.

---

## Mechanization Integration (v1.1.0)

Stage 05 records mechanization metadata from:

- Stage 01 C++ schema validator
- Stage 02 C++ row counter

Mechanization fields appear in the final summary:

```json
"mechanization": {
  "mode": "python+cpp",
  "schema_validator_exit_code": 0,
  "row_counter_exit_code": 0,
  "cpp_compiler_version": "g++-13"
}
```

Mechanization logs are collected from:

```code
logs/mechanization.log
```

More details: [mechanization layer](ca://s?q=Explain_C%2B%2B_mechanization_layer).

---

## Inputs

Stage 05 consumes artifacts produced by earlier stages:

- Stage 01 schema definitions
- Stage 02 cleaned ingestion output (`cleaned_data.csv`)
- Stage 03 quality metrics (`facility_metrics.csv`, `column_profiles.json`, `quality_summary.json`)
- Stage 04 reporting artifacts (`facility_health.csv`, `dataset_summary.json`, `report_index.json`)
- pipeline configuration (`configs/pipeline.yml`)
- mechanization logs + exit codes (v1.1.0)

All inputs must exist before Stage 05 runs.

---

## Outputs

Stage 05 produces:

### `pipeline_summary.json`

A consolidated summary containing:

- `timestamp_start`
- `timestamp_end`
- `duration_seconds`
- `stage_status` (per‑stage success/failure)
- `warnings` (missing artifacts, inconsistencies)
- `final_status`
- mechanization metadata (v1.1.0)

This artifact is used by downstream systems and Stage 06.

---

## Running Stage 05

### Makefile

```bash
make run
```

Runs the full pipeline (Stages 01–05) and writes the summary to the configured output directory.

### Direct CLI

```bash
python run_pipeline.py \
    --config configs/pipeline.yml \
    --output stage05_reports/pipeline_summary.json
```

The runner will:

1. load configuration
2. execute Stages 01–04
3. collect mechanization exit codes
4. validate Stage 04 artifacts
5. generate the summary
6. exit with success or failure

---

## Deterministic Subprocess Execution (v1.1.0)

Stage 05 enforces deterministic subprocess behavior for mechanization:

- fixed command invocation
- stable environment variables
- deterministic exit‑code propagation
- deterministic stderr/stdout capture
- isolation from Python runtime variability

Subprocess failures are surfaced as:

- `MechanizationError`
- non‑zero exit codes
- warnings in the final summary

More details: [subprocess contract](ca://s?q=Explain_deterministic_subprocess_contract).

---

## Validation Behavior

Stage 05 performs several checks:

- presence of Stage 04 artifacts
- valid JSON structure for reporting files
- non‑empty facility‑level and dataset‑level outputs
- consistency between Stage 03 metrics and Stage 04 reports
- manifest completeness (`report_index.json`)
- mechanization exit‑code validation (v1.1.0)

Warnings are included in the summary but do not necessarily stop execution.

---

## Diagnostics

Stage 05 integrates with multi‑stage diagnostics:

- Stage 02 ingestion checks
- Stage 03 intermediate artifact checks
- Stage 04 reporting checks
- cross‑stage consistency checks
- mechanization diagnostics (v1.1.0)

Diagnostics can be run via:

```bash
make diag-intermediate
make diag-pos
make diag-qies
```

These ensure the pipeline is in a valid state before Stage 06 is introduced.

---

## Example Summary (truncated)

```json
{
  "timestamp_start": "2026-07-23T12:41:10Z",
  "timestamp_end": "2026-07-23T12:41:22Z",
  "duration_seconds": 12.4,
  "stage_status": {
    "stage01": "success",
    "stage02": "success",
    "stage03": "success",
    "stage04": "success"
  },
  "mechanization": {
    "mode": "python+cpp",
    "schema_validator_exit_code": 0,
    "row_counter_exit_code": 0,
    "cpp_compiler_version": "g++-13"
  },
  "warnings": [],
  "final_status": "success"
}
```

---

## Troubleshooting

**Missing Stage 04 artifacts**
Ensure Stage 04 has been executed and outputs exist in `data/stage04_processed/`.

**Mechanization failures**
Check `logs/mechanization.log` for deterministic stderr/stdout.

**Incorrect paths**
Verify `configs/pipeline.yml` points to the correct directories.

**Facility ID mismatches**
Stage 03 and Stage 05 normalize `facility_id` to string to avoid type inconsistencies.

**Makefile errors**
Run `make reset` to clear intermediate directories and rebuild.

---

## Roadmap

Stage 05 completes the deterministic pipeline.
Stage 06 will introduce:

- embeddings
- vector search
- RAG
- LLM summarization
- agentic workflows
- AI‑augmented quality checks

These will build directly on Stage 05 outputs.
