# Stage 05 Design — Pipeline Orchestrator (v1.1.1)

Stage 05 is the deterministic control plane of the CMS Data Quality & Ingestion Pipeline.
It executes Stages 01–04 in order, validates their outputs, coordinates logs, and produces the final `pipeline_summary.json` artifact.

Stage 05 does **not** compute new quality metrics.
Its role is orchestration, validation, and provenance.

---

## 1. Purpose of Stage 05

Stage 05 provides:

- **End‑to‑end orchestration** of Stages 01–04
- **Deterministic execution order**
- **Centralized configuration loading**
- **Cross‑stage validation**
- **Final pipeline summary generation**
- **Mechanization provenance integration**
- **Stable runtime + exit‑code reporting**

Unlike Stages 01–04, which are domain‑specific, Stage 05 coordinates the entire system.

---

## 2. Inputs and Outputs

### Inputs

Stage 05 consumes:

- Stage 02 cleaned dataset
- Stage 01 schema
- Stage 03 quality artifacts
- Stage 04 reporting artifacts
- Pipeline configuration:

```code
configs/pipeline.yml
```

### Outputs

Stage 05 produces:

```code
data/stage05_reports/pipeline_summary.json
```

This summary includes:

- stage execution order
- success/failure status
- timestamps
- total pipeline duration
- mechanization provenance
- ingestion shape
- exit codes
- warnings (if any)

Stage 05 does **not** produce its own log file.
Logging remains stage‑scoped:

```text
logs/run_ingestion.log   # Stage 02
logs/schema_loader.log   # Stage 01
logs/quality.log         # Stage 03
logs/runner.log          # Stage 04
logs/mechanization.log   # mechanization provenance
```

---

## 3. Execution Model (v1.1.1)

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

This ordering is frozen and validated in v1.1.1.

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

Configuration is intentionally minimal to keep Stage 05 predictable.

---

## 6. Error Handling Strategy

Stage 05 uses a **fail‑fast** model:

### If a stage fails

- Orchestration stops immediately
- Failure is recorded in the summary
- Diagnostics can be run to identify the issue

### If a stage produces incomplete artifacts

- Stage 05 marks the stage as failed
- Execution stops
- Summary includes missing artifact details

### If configuration is missing or invalid

- Stage 05 aborts before running any stage
- Summary includes configuration error details

This prevents cascading failures and ensures deterministic behavior.

---

## 7. Summary Artifact Design (v1.1.1)

The final output of Stage 05 is:

```code
data/stage05_reports/pipeline_summary.json
```

### Real v1.1.1 fields

```json
{
  "pipeline": "cms-data-quality-and-ingestion",
  "timestamp_start": "2026-09-17T20:21:52.134860",
  "timestamp_end": "2026-09-17T20:25:12.957663",
  "duration_seconds": 200.822803,
  "stages": {
    "stage01": "success",
    "stage02": "success",
    "stage03": "success",
    "stage04": "success",
    "mechanization": {
      "schema_validator": "VALID",
      "ingestion_utils_normalize": "OK",
      "ingestion_utils_delimiter": ",",
      "ingestion_utils_bom": "OK"
    }
  },
  "warnings": [],
  "mechanization": {
    "mode": "python+cpp",
    "cpp_compiler_version": "g++ (placeholder)",
    "stage": "stage05",
    "exit_code": 0,
    "schema_validator_exit_code": 0,
    "row_counter_exit_code": 0
  }
}
```

### Key v1.1.1 metrics

- **Runtime:** 200.82 seconds
- **Ingestion shape:** 44,707 × 474
- **Mechanization mode:** python+cpp
- **Schema validator:** VALID
- **Exit codes:** all zero
- **Warnings:** none

This artifact is the authoritative record of the pipeline run.

---

## 8. Diagnostics Integration

Stage 05 does not run diagnostics automatically.
Diagnostics are executed via:

```bash
make diagnostics
```

Stage 05 diagnostics script:

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

Maintainer: Brian Deng  <br>
Email: <bdeng.data.pipelines@gmail.com>  <br>
GitHub: <https://github.com/bdeng1018>
