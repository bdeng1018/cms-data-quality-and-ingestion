# Architecture Overview - CMS Data Quality & Ingestion Pipeline

This document describes the high‑level architecture of the CMS Data Quality & Ingestion Pipeline.
It explains how the system is structured, how each stage interacts, and how data flows from raw ingestion to final reporting.

This document describes both the pipeline architecture and the deployment architecture that supports runtime execution, security, observability, and infrastructure provisioning.

---

## 1. Architectural Goals

The pipeline is designed to:

- Ingest CMS POS/QIES data reliably
- Apply deterministic cleaning and normalization
- Enforce schema consistency across all stages
- Produce validated intermediate artifacts
- Generate reproducible quality reports
- Provide a Stage 05 orchestrator for full end‑to‑end execution
- Support diagnostics at every stage
- Maintain strict separation between code, configs, data, and diagnostics

The architecture also includes a deterministic deployment layer providing containerization, orchestration, security, observability, and infrastructure provisioning.
The architecture emphasizes **clarity**, **traceability**, and **reproducibility**.

---

## 2. High‑Level Pipeline Flow

```text
Raw Data → Stage 02 → Cleaned Data → Stage 03 → Quality Artifacts → Stage 04 → Reports → Stage 05 → Pipeline Summary
```

Each stage is independent, testable, and diagnosable.

---

## 3. Stage Architecture

### Stage 01 — Schema Definition

- Regenerates `schema.json` from cleaned Stage 02 data.
- Ensures downstream stages operate on a consistent column set.
- Includes diagnostics verifying schema integrity.

**Inputs:** `data/stage02_cleaned/cleaned_data.csv`  
**Outputs:** `data/stage01_schema/schema.json`

---

### Stage 02 — Raw Ingestion + Cleaning

- Fetches POS data from API.
- Ingests POS/QIES into parquet/csv.
- Applies deterministic cleaning rules.
- Produces canonical cleaned dataset.

**Inputs:** Raw POS/QIES files  
**Outputs:**  

- `data/stage02_raw/`  
- `data/stage02_cleaned/cleaned_data.csv`

---

### Stage 03 — Data Quality Profiling

- Runs quality checks on cleaned data.
- Generates intermediate artifacts (metrics, flags, distributions).
- Includes diagnostics validating quality outputs.

**Inputs:** Cleaned data  
**Outputs:** `data/stage03_intermediate/`

---

### Stage 04 — Reporting

- Consumes Stage 03 artifacts.
- Generates formatted reports (CSV/JSON/Markdown).
- Includes diagnostics verifying report completeness.

**Inputs:** Intermediate artifacts  
**Outputs:** `data/stage04_processed/`

---

### Stage 05 — Pipeline Runner (Orchestrator)

- Executes Stages 01–04 in order.
- Loads configuration from `configs/pipeline.yml`.
- Writes a final pipeline summary artifact.
- Includes diagnostics validating the full pipeline run.

**Inputs:** All previous stage outputs  
**Outputs:**  

- `data/stage05_reports/`  
- `data/stage05_reports/pipeline_summary.json`

---

## 4. Directory Structure

```text
src/
  stage01_schema_definition/
  stage02_raw_ingestion/
  stage03_data_quality/
  stage04_reporting/
  stage05_pipeline_runner/

scripts/
  diagnostics/
    stage01/
    stage02/
    stage03/
    stage04/
    stage05/

configs/
data/
logs/
tests/
docs/
deployment/
.vscode/
Makefile
```

This structure enforces strict separation of:

- **Code** (`src/`)
- **Diagnostics** (`scripts/diagnostics/`)
- **Configuration** (`configs/`)
- **Artifacts** (`data/`)
- **Developer documentation** (`docs/`)
- **Deployment** (`deployment/`)
- **Tooling** (`.vscode/`)
- **Build orchestration** (`Makefile`)

The `deployment/` directory defines the runtime architecture, including CI/CD, environment configuration, containerization, Kubernetes manifests, Helm packaging, Terraform infrastructure, logging, monitoring, and security.

---

## 5. Configuration Architecture

All pipeline configuration lives in:

```code
configs/pipeline.yml
```

Key responsibilities:

- Define output directories
- Configure logging paths
- Provide stage‑specific parameters
- Support Stage 05 orchestration

Configuration is intentionally minimal and declarative.

---

## 6. Diagnostics Architecture

Every stage includes a dedicated diagnostics module:

```code
scripts/diagnostics/<stage>/
```

Diagnostics validate:

- Input availability
- Output correctness
- Schema consistency
- Artifact completeness
- Logical invariants

Diagnostics are runnable independently or via:

```bash
make diagnostics
```

This ensures the pipeline is always in a valid state.

---

## 7. Makefile Architecture

The Makefile provides:

- Stage runners (`make stage01` → `make stage05`)
- Individual ingestion utilities
- Full diagnostics (`make diagnostics`)
- Testing (`make test`)
- Linting (`make lint`)
- Safe cleanup (`make clean-cache`)
- Artifact reset (`make reset`)
- Environment setup (`make env`)

It is the primary developer interface for running the pipeline.

---

## 8. Logging Architecture

The pipeline uses stage‑specific log files:

```text
logs/ingestion.log        # Stage 02
logs/quality.log          # Stage 03
logs/runner.log           # Stage 04
```

Stage 05 does not create a new log file.
Instead, it produces a final summary artifact:

```text
data/stage05_reports/pipeline_summary.json
```

This summary captures:

- stage execution order
- success/failure status
- timestamps
- total pipeline duration

Logging remains stage‑scoped, while Stage 05 focuses on orchestration and summarization.

---

## 9. Testing Architecture

All tests live in:

```code
tests/
```

Tests cover:

- Stage logic
- Diagnostics behavior
- Schema consistency
- Reporting correctness
- Pipeline runner orchestration

Run via:

```bash
make test
```

---

## 10. Extensibility

The architecture supports:

- Adding new stages
- Adding new diagnostics
- Adding new ingestion sources
- Adding new reporting formats
- Adding new pipeline configurations
- Extending deployment subsystems (Helm, k8s, Terraform, monitoring, security)

Each stage is isolated, making extension straightforward.

---

## 11. Deployment Architecture

The CMS Data Quality & Ingestion Pipeline includes a full deployment layer
responsible for runtime execution, containerization, orchestration, security,
observability, and infrastructure provisioning.

Deployment supports multiple environments:

- local development
- docker-compose
- Kubernetes (k8s)
- Helm-based packaging
- Terraform-managed infrastructure

Deployment behavior is defined in:

- `deployment/DEPLOYMENT.md` — runtime architecture
- `deployment/OPERATIONS.md` — operational rules
- `deployment/CONTRACTS.md` — deterministic deployment contracts

The deployment layer ensures reproducible execution across all environments.

---

## 12. Provenance Architecture

The pipeline maintains deterministic provenance across all layers. Provenance
tracks version fields that describe the state of the system at every run:

```text
pipeline_version
schema_version
artifact_version
manifest_version
deployment_version
sbom_version
```

These fields are written into:

- manifest.provenance
- SBOM metadata
- release notes
- audit logs

Provenance ensures traceability, reproducibility, and compliance across pipeline
execution, deployment changes, and artifact generation.

Reference documents:

- `deployment/MANIFEST_SPEC.md`
- `deployment/SBOM.md`
- `deployment/VERSIONING.md`

---

## 13. Governance & Compliance Architecture

The pipeline includes a deterministic control plane governing:

- change approval
- compliance enforcement
- risk modeling
- audit logging
- access control

These rules ensure the system behaves consistently and predictably across all
environments.

Control plane documents:

- `deployment/GOVERNANCE.md`
- `deployment/COMPLIANCE.md`
- `deployment/RISK_MODEL.md`
- `deployment/AUDIT_LOGS.md`
- `deployment/ACCESS_CONTROL.md`

Governance and compliance integrate with CI/CD, provenance, and deployment
validation.

---

## 14. Deployment Directory Structure

The deployment layer is organized into subsystem directories:

```text
deployment/
  ci/            # CI/CD workflows and validation
  env/           # environment variable definitions
  helm/          # Helm chart and values
  k8s/           # Kubernetes manifests
  terraform/     # infrastructure provisioning
  logging/       # logging configuration
  monitoring/    # metrics, alerts, dashboards
  security/      # hardening and security policies
```

Each subsystem maps to a specific part of the runtime architecture:

- **ci/** — GitHub Actions workflows, validation rules  
- **env/** — deterministic environment configuration  
- **helm/** — packaged deployment for Kubernetes  
- **k8s/** — raw manifests for direct cluster deployment  
- **terraform/** — infrastructure provisioning and drift detection  
- **logging/** — Fluent Bit configuration and log routing  
- **monitoring/** — Prometheus, Grafana, SLO/SLI contracts  
- **security/** — hardening rules, network policies, RBAC alignment

This structure ensures deployment is modular, reproducible, and fully aligned
with the pipeline’s architecture.

---

## 15. Contact

Maintainer: Brian Deng <br>
Email: <bdeng.data.pipelines@gmail.com> <br>
GitHub: <https://github.com/bdeng1018>
