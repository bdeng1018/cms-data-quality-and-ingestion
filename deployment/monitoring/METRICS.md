# CMS Data Quality & Ingestion Pipeline — Metrics Contract

## Documentation Contract

This document defines the deterministic metrics contract for the CMS Data Quality
& Ingestion Pipeline. These metrics provide reproducible observability across
local development, docker-compose, Kubernetes, Helm, and cloud deployments.

### Determinism Guarantees

- stable metric names  
- stable metric categories  
- stable units and semantics  
- stable provenance fields  
- reproducible metric generation  

### Side Effects

- exposes ingestion latency  
- exposes artifact generation counts  
- exposes diagnostics results  
- exposes log volume behavior  

---

## Metric Categories

The pipeline exposes four deterministic metric categories:

1. **Ingestion Latency Metrics**  
2. **Artifact Generation Metrics**  
3. **Diagnostics Metrics**  
4. **Log Volume Metrics**

Each category is designed to be stable, reproducible, and provenance-aware.

---

## Ingestion Latency Metrics

These metrics measure how long ingestion stages take.

### **Metric: `cms_pipeline_runtime_seconds`**

- **Type:** Gauge  
- **Unit:** seconds  
- **Meaning:** Total runtime of the pipeline  
- **Deterministic Contract:**  
  - must be monotonic per run  
  - must reset between runs  
  - must be recorded in manifest.provenance  

### **Metric: `cms_stage_runtime_seconds{stage="01"}`**

- **Type:** Gauge  
- **Unit:** seconds  
- **Meaning:** Runtime of Stage 01 ingestion  
- **Deterministic Contract:**  
  - stable stage labels  
  - stable units  
  - stable naming  

Stages 02–05 follow the same pattern.

---

## Artifact Generation Metrics

These metrics measure how many artifacts the pipeline produces.

### **Metric: `cms_pipeline_artifacts_generated_total`**

- **Type:** Counter  
- **Unit:** count  
- **Meaning:** Number of artifacts generated in Stage 04  
- **Deterministic Contract:**  
  - must increment deterministically  
  - must match artifact registry  
  - must be validated in CI/CD  

### **Metric: `cms_artifact_bytes_total`**

- **Type:** Counter  
- **Unit:** bytes  
- **Meaning:** Total size of generated artifacts  
- **Deterministic Contract:**  
  - stable byte units  
  - stable naming  
  - stable provenance  

---

## Diagnostics Metrics

These metrics measure validation and diagnostics outcomes.

### **Metric: `cms_pipeline_diagnostics_passed_total`**

- **Type:** Counter  
- **Unit:** count  
- **Meaning:** Number of diagnostics checks passed  
- **Deterministic Contract:**  
  - must match diagnostics report  
  - must be validated in CI/CD  

### **Metric: `cms_pipeline_diagnostics_failed_total`**

- **Type:** Counter  
- **Unit:** count  
- **Meaning:** Number of diagnostics checks failed  
- **Deterministic Contract:**  
  - must be stable  
  - must be reproducible  
  - must be included in manifest.provenance  

---

## Log Volume Metrics

These metrics measure log throughput and pipeline activity.

### **Metric: `cms_pipeline_log_lines_total`**

- **Type:** Counter  
- **Unit:** count  
- **Meaning:** Total number of log lines emitted  
- **Deterministic Contract:**  
  - must be monotonic  
  - must reset per run  
  - must match Fluent Bit ingestion  

### **Metric: `rate(cms_pipeline_log_lines_total[1m])`**

- **Type:** Rate  
- **Unit:** lines/min  
- **Meaning:** Log throughput  
- **Deterministic Contract:**  
  - stable rate window  
  - stable units  
  - used for alerting  

---

## Provenance Mapping

All metrics must include deterministic provenance labels:

- `provenance_environment`  
- `provenance_executor`  
- `pipeline_version`  

These labels ensure metrics can be traced across:

- local  
- docker-compose  
- Kubernetes  
- Helm  
- cloud  

---

## Reproducibility Contract

Metrics **must**:

- use pinned names  
- use pinned units  
- use pinned labels  
- avoid nondeterministic increments  
- avoid nondeterministic resets  
- be validated in CI/CD  
- be included in manifest.provenance  

This ensures observability behaves identically across all environments.

---

## Future Extensions

- distributed ingestion metrics  
- cloud storage ingestion metrics  
- RAG/AI indexing metrics  
- ingestion SLA metrics  
- ingestion SLO/SLI definitions  
- multi-region ingestion metrics  
