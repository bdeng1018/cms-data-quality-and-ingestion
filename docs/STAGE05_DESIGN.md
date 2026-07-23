# Stage 05 Design — Pipeline Orchestrator

Stage 05 is the control plane of the CMS Data Quality & Ingestion Pipeline.  
It is responsible for executing Stages 01–04 in order, validating their outputs, coordinating logs, and producing a final pipeline summary artifact.

This document describes the design, responsibilities, execution model, and error‑handling strategy of Stage 05.

---

## 1. Purpose of Stage 05

Stage 05 provides:

- **End‑to‑end orchestration** of the entire pipeline  
- **Deterministic execution order**  
- **Centralized configuration loading**  
- **Cross‑stage validation**  
- **Final pipeline summary generation**  
- **Integration with diagnostics**  

Unlike Stages 01–04, which are domain‑specific and self‑contained, Stage 05 is responsible for coordinating the entire system.

---

## 2. Inputs and Outputs

### Inputs

Stage 05 consumes:

- Cleaned data from Stage 02  
- Schema from Stage 01  
- Intermediate artifacts from Stage 03  
- Reports from Stage 04  
- Configuration from:

```code
configs/pipeline.yml
```

### Outputs

Stage 05 produces:

```code
data/stage05_reports/pipeline_summary.json
```

This summary includes:

- Stage execution order  
- Success/failure status  
- Timestamps  
- Total pipeline duration  
- Any warnings surfaced during execution  

Stage 05 does **not** produce its own log file.  
Logging remains stage‑scoped:

```code
logs/ingestion.log        # Stage 02
logs/quality.log          # Stage 03
logs/runner.log           # Stage 04
```

---

## 3. Execution Model

Stage 05 executes the pipeline in the following order:

```text
Stage 02 → Stage 01 → Stage 03 → Stage 04
```

This ordering is intentional:

### Why Stage 02 runs before Stage 01

Stage 01 regenerates `schema.json` from cleaned Stage 02 data.  
Therefore, Stage 02 must run first.

### Why Stage 03 runs after Stage 01  

Stage 03 quality checks depend on the schema produced by Stage 01.

### Why Stage 04 runs after Stage 03  

Stage 04 reports depend on Stage 03 intermediate artifacts.

---

## 4. Orchestration Flow

The orchestrator follows this flow:

```text
Load config
↓
Start timer
↓
Run Stage 02
↓
Run Stage 01
↓
Run Stage 03
↓
Run Stage 04
↓
Validate outputs
↓
Generate pipeline summary
↓
Stop timer
↓
Write summary to stage05_reports/
```

Each step is validated before moving to the next.

---

## 5. Configuration Loading

Stage 05 loads configuration from:

```code
configs/pipeline.yml
```

Required fields:

```yaml
stage05:
  output_dir: "data/stage05_reports"
```

Optional fields:

- custom report names
- custom artifact paths
- execution flags
- future stage parameters

Configuration is intentionally minimal to keep Stage 05 simple and predictable.

---

## 6. Error Handling Strategy

Stage 05 uses a **fail‑fast** model:

### If a stage fails

- The orchestrator stops immediately
- The failure is recorded in the summary
- Diagnostics can be run to identify the issue

### If a stage produces incomplete artifacts

- Stage 05 marks the stage as failed
- Execution stops
- Summary includes missing artifact details

### If configuration is missing or invalid

- Stage 05 aborts before running any stage
- Summary includes configuration error details

This ensures pipeline correctness and prevents cascading failures.

---

## 7. Summary Artifact Design

The final output of Stage 05 is:

```code
data/stage05_reports/pipeline_summary.json
```

Recommended structure:

```json
{
  "pipeline": "cms-data-quality-and-ingestion",
  "timestamp_start": "2026-07-22T17:54:00",
  "timestamp_end": "2026-07-22T17:54:42",
  "duration_seconds": 42.3,
  "stages": {
    "stage02": "success",
    "stage01": "success",
    "stage03": "success",
    "stage04": "success"
  },
  "warnings": []
}
```

This artifact is the authoritative record of the pipeline run.

---

## 8. Diagnostics Integration

Stage 05 does not run diagnostics automatically.
Instead, diagnostics are executed via:

```bash
make diagnostics
```

Stage 05’s own diagnostics script:

```code
scripts/diagnostics/stage05/check_pipeline.py
```

Validates:

- configuration loading
- presence of Stage 05 summary
- presence of Stage 04 reports
- presence of Stage 03 artifacts
- presence of Stage 01 schema
- presence of Stage 02 cleaned data

This ensures the pipeline is fully consistent.

---

## 9. Extensibility

Stage 05 is designed to support:

- additional stages
- branching logic
- conditional execution
- multiple report formats
- multiple ingestion sources
- future pipeline configurations

Adding a new stage requires:

1. A new folder under `src/`
2. A new diagnostics module
3. A new Makefile target
4. Updating Stage 05 execution order
5. Updating the summary artifact

The orchestrator is intentionally simple to keep extension predictable.

---

## 10. Contact

Maintainer: Brian Deng <br>
Email: <bdeng.data.pipelines@gmail.com> <br>
GitHub: <https://github.com/bdeng1018>
