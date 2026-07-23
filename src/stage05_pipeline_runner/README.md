# Stage 05 — Pipeline Runner & Summary Generator

Stage 05 provides the orchestration layer for the CMS POS/QIES ingestion and data‑quality pipeline. It coordinates Stages 01–04, validates required artifacts, and produces a final summary report describing the overall pipeline execution.

Stage 05 marks the completion of the deterministic pipeline in Branch 1.
Stage 06 will introduce AI/RAG/agentic augmentation on top of these outputs.

---

## Overview

Stage 05 is responsible for:

- Running Stages 01–04 in sequence
- Validating that Stage 04 reporting artifacts are complete
- Producing a consolidated pipeline summary (`pipeline_summary.json`)
- Emitting warnings for missing or inconsistent artifacts
- Providing a single entry point for full‑pipeline execution
- Integrating with Makefile targets for reproducible runs

This stage does not modify data. It verifies, orchestrates, and summarizes.

---

## Inputs

Stage 05 consumes artifacts produced by earlier stages:

- Stage 01 schema definitions
- Stage 02 cleaned ingestion output (c`leaned_data.csv`)
- Stage 03 quality metrics (`facility_metrics.csv`, `column_profiles.json`, `quality_summary.json`)
- Stage 04 reporting artifacts (`facility_health.csv`, `dataset_summary.json`, `report_index.json`)
- Pipeline configuration file (`configs/pipeline.yml`)

All inputs must exist before Stage 05 runs.

---

## Outputs

Stage 05 produces:

`pipeline_summary.json`

A consolidated summary containing:

- `timestamp_start`
- `timestamp_end`
- `duration_seconds`
- `stage_status` (per‑stage success/failure)
- `warnings` (missing artifacts, inconsistencies)
- `final_status` (overall pipeline result)

This artifact is used by downstream systems and Stage 06.

---

## Running Stage 05

### Makefile

```bash
make run
```

Runs the full pipeline (Stages 01–05) and writes the summary to the configured output directory.

### Direct CLI

```code
python run_pipeline.py \
    --config configs/pipeline.yml \
    --output stage05_reports/pipeline_summary.json
```

The runner will:

1. Load configuration
2. Execute Stages 01–04
3. Validate Stage 04 artifacts
4. Generate the summary
5. Exit with success or failure

---

## Validation Behavior

Stage 05 performs several checks:

- Presence of Stage 04 artifacts
- Valid JSON structure for reporting files
- Non‑empty facility‑level and dataset‑level outputs
- Consistency between Stage 03 metrics and Stage 04 reports
- Manifest completeness (`report_index.json`)

Warnings are included in the summary but do not necessarily stop execution.

---

## Diagnostics

Stage 05 integrates with multi‑stage diagnostics:

- Stage 02 ingestion checks
- Stage 03 intermediate artifact checks
- Stage 04 reporting checks
- Cross‑stage consistency checks

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
  "warnings": [],
  "final_status": "success"
}
```

---

## Troubleshooting

**Missing Stage 04 artifacts**

Ensure Stage 04 has been executed and outputs exist in `data/stage04_processed/`.

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

- Embeddings
- Vector search
- RAG
- LLM summarization
- Agentic workflows
- AI‑augmented quality checks

These will build directly on Stage 05 outputs.
