# Documentation Index — CMS Data Quality & Ingestion Pipeline

A structured entry point for all documentation in the **cms-data-quality-and-ingestion** deterministic pipeline.  
Use this index to navigate architecture, onboarding, data contracts, stage documentation, deployment, and future roadmap.

---

## 1. High‑Level Documentation

### [README.md](../README.md)

Project overview, goals, quickstart, and repository structure.

### [ONBOARDING.md](ONBOARDING.md)

Developer setup, environment configuration, Makefile workflow, and local development instructions.

### [ARCHITECTURE.md](ARCHITECTURE.md)

High‑level system design, stage responsibilities, directory layout, logging, configuration, and testing architecture.

### [PIPELINE_FLOW.md](PIPELINE_FLOW.md)

End‑to‑end data flow, artifact flow, stage transitions, and diagnostics execution.

### [ROADMAP.md](ROADMAP.md)

Future development plan for Branch 1 and Branch 2, including Stage 06–08 boundaries.

---

## 2. Data Contract Documentation

### [DATA_DICTIONARY.md](DATA_DICTIONARY.md)

Definitions for all fields in Stage 02 cleaned datasets, including types, descriptions, and semantic meaning.

### [SCHEMA_REFERENCE.md](SCHEMA_REFERENCE.md)

Reference for Stage 01 schema definitions, required fields, types, and schema evolution rules.

### [GLOSSARY.md](GLOSSARY.md)

Canonical definitions for pipeline terminology, POS/QIES concepts, and deployment vocabulary.

---

## 3. Stage‑Specific Documentation

### Stage 01 — Schema Definition  

[src/stage01_schema_definition/README.md](../src/stage01_schema_definition/README.md)  
Schema loading, validation rules, and canonical field definitions.

### Stage 02 — Raw Ingestion  

[src/stage02_raw_ingestion/README.md](../src/stage02_raw_ingestion/README.md)  
Raw file ingestion, structural validation, and canonical dataset creation.

### Stage 03 — Data Quality  

[src/stage03_data_quality/README.md](../src/stage03_data_quality/README.md)  
Null checks, duplicate detection, sparsity analysis, drift indicators, and quality metrics.

### Stage 04 — Reporting  

[src/stage04_reporting/README.md](../src/stage04_reporting/README.md)  
Report generation, summary artifacts, and quality metric aggregation.

### Stage 05 — Pipeline Runner  

[STAGE05_DESIGN.md](STAGE05_DESIGN.md)  
Execution order, configuration loading, error handling, summary generation, and cross‑stage coordination.  
[src/stage05_pipeline_runner/README.md](../src/stage05_pipeline_runner/README.md)

---

## 4. Deployment & Operations Documentation

### [deployment/DEPLOYMENT.md](../deployment/DEPLOYMENT.md)

Deployment architecture, containerization, CI/CD, Terraform modules, and environment setup.

### [deployment/OPERATIONS.md](../deployment/OPERATIONS.md)

Operational procedures, logs, monitoring, provenance validation, and runtime behavior.

### [deployment/MANIFEST_SPEC.md](../deployment/MANIFEST_SPEC.md)

Specification for pipeline manifests, metadata, and deterministic output guarantees.

### [deployment/security/HARDENING.md](../deployment/security/HARDENING.md)

Security posture, container hardening, least‑privilege rules, and compliance requirements.

### [deployment/monitoring/OBSERVABILITY.md](../deployment/monitoring/OBSERVABILITY.md)

Metrics, logs, traces, dashboards, and SLO/SLI definitions.

---

## 5. Project Governance Documentation

### [CONTRIBUTING.md](../CONTRIBUTING.md)

Contribution guidelines, PR workflow, coding standards, and branching strategy.

### [STYLE_GUIDE.md](STYLE_GUIDE.md)

Coding conventions, deterministic rules, directory structure, Makefile standards, and testing guidelines.

### [CHANGELOG.md](../CHANGELOG.md)

Version history and release notes.

### [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md)

Community and contributor behavior guidelines.

### [SECURITY.md](../SECURITY.md)

Security reporting process and vulnerability disclosure guidelines.

---

## 6. Visual Diagrams

### [pipeline_architecture](../diagrams/pipeline_architecture.md)

High‑level pipeline architecture diagram.

### [schema_overview](../diagrams/schema_overview.md)

Schema visualization for Stage 01 and Stage 02 outputs.

---

## 7. Navigation Guidance

### If you're evaluating the pipeline

- Start with **README.md**  
- Then read **ARCHITECTURE.md**  
- Follow with **PIPELINE_FLOW.md**  
- Review **DATA_DICTIONARY.md** and **SCHEMA_REFERENCE.md**  
- Finish with **STAGE05_DESIGN.md**

### If you're onboarding as a developer

- Start with **ONBOARDING.md**  
- Explore the `src/` stage folders  
- Use diagnostics under `scripts/diagnostics/`  
- Run tests under `tests/`

---

## 8. Maintainer

Maintainer: **Brian Deng**  
Email: **<bdeng.data.pipelines@gmail.com>**  
GitHub: **<https://github.com/bdeng1018>**
