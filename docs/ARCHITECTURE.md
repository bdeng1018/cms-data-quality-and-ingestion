# Architecture Overview - CMS Data Quality & Ingestion Pipeline

The CMS Data Quality & Ingestion Pipeline is a deterministic, contract‑driven system for ingesting, validating, profiling, and reporting on CMS POS/QIES data.

This document describes the **pipeline architecture** (Stages 01–05) and the **deployment architecture** (containerization, CI/CD, Terraform, observability, security) that ensures reproducible runtime behavior across all environments.

---

## 1. Architectural Goals

The pipeline is designed to:

- Ingest CMS POS/QIES data reliably
- Apply deterministic cleaning and normalization
- Enforce strict schema consistency
- Produce validated intermediate artifacts
- Generate reproducible quality reports
- Provide a Stage 05 orchestrator for full end‑to‑end execution
- Expose diagnostics at every stage
- Maintain strict separation between code, configs, data, and diagnostics
- Support deterministic deployment across local, Docker, Compoase, and CI/CD

The architecture emphasizes **clarity**, **traceability**, **reproducibility**, and **audit-friendly behavior**.

---

## 2. High‑Level Pipeline Flow

```text
Raw Data → Stage 02 → Cleaned Data → Stage 01 → Schema → Stage 03 → Quality Artifacts → Stage 04 → Reports → Stage 05 → Pipeline Summary
```

Each stage is independent, testable, diagnosable, and produces deterministics artifacts.

---

## 3. Stage Architecture

### Stage 01 — Schema Definition & Validation

- Regenerates `schema.json` from cleaned Stage 02 data.
- Validates schema deterministrically (Python + C++).
- Ensures column count, order, and naming.
- Provides diagnostics verifying schema integrity.

**Inputs:** `data/stage02_cleaned/cleaned_data.csv`
**Outputs:** `data/stage01_schema/schema.json`

---

### Stage 02 — Raw Ingestion + Cleaning

- Fetches POS data from API.
- Ingests POS/QIES into parquet/CSV.
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

**Inputs:** Cleaned data + schema
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

- Executes Stages 01–04 deterministically.
- Loads configuration from `configs/pipeline.yml`.
- Writes final pipeline summary.
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
  utils_cpp/

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
- **Documentation** (`docs/`)
- **Deployment** (`deployment/`)
- **Tooling** (`.vscode/`)
- **Build orchestration** (`Makefile`)

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

Configuration is minimal, declarative, and deterministic.

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

Run all diagnostics:

```bash
make diagnostics
```

Diagnostics never mutate source data.

---

## 7. Makefile Architecture

The Makefile provides deterministic orchestration:

- Stage runners (`make stage01` → `make stage05`)
- Ingestion utilities
- Full diagnostics (`make diagnostics`)
- Testing (`make test`)
- Linting (`make lint`)
- Safe cleanup (`make clean-cache`)
- Artifact reset (`make reset`)
- Environment setup (`make env`)
- C++ builds (`make cpp-all`)

The Makefile is the primary developer interface.

---

## 8. Logging Architecture

Stage-specific logs:

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

Logging remains stage‑scoped, while Stage 05 focuses on orchestration.

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
- C++ mechanization utilities

Run tests:

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
- Extending deployment subsystems
- Adding AI/RAG stages (future Stage 06-08)

Each stage is isolated, making extension straightforward.

---

## 11. Deployment Architecture

The deployment layer provides deterministic runtime behavior across:

- local development
- Docker
- docker-compose
- Kubernetes
- Helm
- Terraform

Deployment behavior is defined in:

- [`deployment/DEPLOYMENT.md`](../deployment/DEPLOYMENT.md) — runtime architecture
- [`deployment/OPERATIONS.md`](../deployment/OPERATIONS.md) — operational rules
- [`deployment/CONTRACTS.md`](../deployment/CONTRACTS.md) — deterministic deployment contracts

The deployment layer ensures reproducible execution across all environments.

---

## 12. Provenance Architecture

The pipeline maintains deterministic provenance across all layers. Version fields include:

```text
pipeline_version
schema_version
artifact_version
manifest_version
deployment_version
sbom_version
```

These fields appear in:

- manifests
- SBOM metadata
- release notes
- audit logs

Reference documents:

- [`deployment/MANIFEST_SPEC.md`](../deployment/MANIFEST_SPEC.md)
- [`deployment/SBOM.md`](../deployment/SBOM.md)
- [`deployment/VERSIONING.md`](../deployment/VERSIONING.md)

---

## 13. Governance & Compliance Architecture

The control plane governs:

- change approval
- compliance enforcement
- risk modeling
- audit logging
- access control

These rules ensure the system behaves consistently and predictably across all
environments.

Documents:

- [`deployment/GOVERNANCE.md`](../deployment/GOVERNANCE.md)
- [`deployment/COMPLIANCE.md`](../deployment/COMPLIANCE.md)
- [`deployment/RISK_MODEL.md`](../deployment/RISK_MODEL.md)
- [`deployment/AUDIT_LOGS.md`](../deployment/AUDIT_LOGS.md)
- [`deployment/ACCESS_CONTROL.md`](../deployment/ACCESS_CONTROL.md)

Governance integrates with CI/CD, provenance, and deployment
validation.

---

## 14. Deployment Directory Structure

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

Subsystem responsibilities:

- **ci/** — CI/CD workflows
- **env/** — deterministic environment configuration
- **helm/** — packaged Kubernetes deployment
- **k8s/** — raw manifests
- **terraform/** — infrastructure provisioning
- **logging/** — Fluent Bit routing
- **monitoring/** — Prometheus, Grafana, SLO/SLI
- **security/** — hardening, RBAC, policies

This structure ensures modular, reproducible deployment.

---

## 15. Contact

Maintainer: Brian Deng <br>
Email: <bdeng.data.pipelines@gmail.com> <br>
GitHub: <https://github.com/bdeng1018>
