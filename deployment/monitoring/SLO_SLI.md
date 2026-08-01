# CMS Data Quality & Ingestion Pipeline — SLO/SLI Contract

## Documentation Contract

This document defines the deterministic Service Level Indicators (SLIs) and
Service Level Objectives (SLOs) for the CMS Data Quality & Ingestion Pipeline.
These guarantees ensure reproducible ingestion behavior, predictable latency,
stable artifact generation, and reliable diagnostics across all environments.

### Determinism Guarantees

- pinned SLI definitions  
- pinned SLO thresholds  
- pinned units and semantics  
- pinned provenance labels  
- reproducible measurement windows  

### Side Effects

- enforces ingestion performance  
- enforces artifact generation reliability  
- enforces diagnostics stability  
- enforces log throughput consistency  

---

## SLI Definitions (Deterministic)

SLIs define *what* is measured. All SLIs must be:

- deterministic  
- reproducible  
- provenance-aware  
- environment-agnostic  

### SLI: Ingestion Latency

```code
SLI_ingestion_latency = cms_pipeline_runtime_seconds
```

Measures total pipeline runtime.

### SLI: Artifact Generation Count

```code
SLI_artifacts_generated = cms_pipeline_artifacts_generated_total
```

Measures number of artifacts produced.

### SLI: Diagnostics Pass Rate

```code
SLI_diagnostics_pass_rate =
    cms_pipeline_diagnostics_passed_total /
    (cms_pipeline_diagnostics_passed_total + cms_pipeline_diagnostics_failed_total)
```

### SLI: Log Throughput

```code
SLI_log_throughput = rate(cms_pipeline_log_lines_total[1m])
```

---

## SLO Targets (Deterministic)

SLOs define *the target* for each SLI. These thresholds are pinned and
environment‑independent.

### SLO: Ingestion Latency

```code
SLO_ingestion_latency <= 300 seconds
```

The pipeline must complete within **5 minutes**.

### SLO: Artifact Generation

```code
SLO_artifacts_generated >= 1 artifact per run
```

Pipeline must produce at least one Stage 04 artifact.

### SLO: Diagnostics Pass Rate

```code
SLO_diagnostics_pass_rate >= 0.95
```

At least **95%** of diagnostics must pass.

### SLO: Log Throughput

```code
SLO_log_throughput >= 10 lines/min
```

Pipeline must emit at least **10 log lines per minute**.

---

## Error Budget Model

The error budget defines how much deviation from SLOs is acceptable.

### Error Budget Calculation

```code
error_budget = 1.0 - SLO_target
```

Examples:

- Diagnostics SLO = 0.95 → error budget = 0.05  
- Artifact SLO = 1.0 → error budget = 0.0 (no tolerance)  
- Latency SLO = 300s → error budget = 0s (strict threshold)  

### Error Budget Burn

Error budget is considered “burned” when:

- latency exceeds threshold  
- artifacts are missing  
- diagnostics fail  
- log throughput drops  

Burn events must be logged and included in provenance.

---

## Measurement Windows

All SLIs must be measured over deterministic windows:

- **1m** for log throughput  
- **5m** for ingestion latency  
- **per-run** for artifact generation  
- **per-run** for diagnostics  

These windows are pinned and must not change without version bump.

---

## Provenance Mapping

All SLI/SLO measurements must include:

- `provenance_environment`  
- `provenance_executor`  
- `pipeline_version`  
- `run_id` (future)  
- `timestamp`  

This ensures SLO compliance is reproducible across:

- local  
- docker-compose  
- Kubernetes  
- Helm  
- cloud  

---

## Reproducibility Contract

SLO/SLI measurement **must**:

- use pinned metric names  
- use pinned units  
- use pinned thresholds  
- avoid nondeterministic resets  
- avoid nondeterministic windows  
- be validated in CI/CD  
- be included in manifest.provenance  

This ensures observability behaves identically across all environments.

---

## Future Extensions

- ingestion SLA definitions  
- distributed ingestion SLOs  
- cloud storage ingestion SLOs  
- RAG/AI indexing SLOs  
- multi-region ingestion SLOs  
- OpenTelemetry tracing SLIs  
