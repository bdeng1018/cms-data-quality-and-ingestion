# Developer Onboarding — CMS Data Quality & Ingestion Pipeline

Welcome to the CMS Data Quality & Ingestion Pipeline.  
This document provides everything you need to set up your environment, run the pipeline, debug issues, and contribute code.

---

## 1. Prerequisites

Install the following:

- Python 3.11+
- Conda (recommended)
- VS Code
- Git

Clone the repository:

```bash
git clone https://github.com/bdeng1018/cms-data-quality-and-ingestion
cd cms-data-quality-and-ingestion
```

---

## 2. VS Code Workspace Setup

Open the workspace file at the repo root:

```code
cms-data-ingestion.code-workspace
```

This loads:

- `.vscode/settings.json`
- `.vscode/tasks.json`
- `.vscode/launch.json`
- `.vscode/extensions.json`

### Recommended Extensions

These are auto-loaded:

- Python + Pylance
- Black
- Ruff
- Pytest
- Rainbow CSV
- YAML Support
- Makefile Tools
- GitLens

---

## 3. Environment Setup

Create the environment:

```bash
make env
```

Activate it:

```bash
conda activate pos_qies_pipeline
```

Install local dependencies:

```bash
pip install -e .
```

---

## 4. Running the Pipeline (Stages 01–05)

### Stage 01 — Schema Definition

```bash
make stage01
```

### Stage 02 — Raw Ingestion + Cleaning

```bash
make stage02
```

### Stage 03 — Data Quality Profiling

```bash
make stage03
```

### Stage 04 — Reporting

```bash
make stage04
```

### Stage 05 - Pipeline Runner (Orchestrator)

```bash
make stage05
```

---

## 5. Diagnostics (All Stages)

Run all diagnostics:

```bash
make diagnostics
```

Run individual diagnostics:

```bash
make schema-diagnostics
make diag-pos
make diag-qies FILE=<path>
make diag-cleaned
make diag-quality
make diag-intermediate
make diag-stage04
make diag-pipeline
```

---

## 6. Testing & Linting

Run tests:

```bash
make test
```

Run linting:

```bash
make lint
```

Tests should always be run **before** linting.

---

## 7. Resetting Pipeline Artifacts

### Safe cleanup (recommended)

```bash
make clean-cache
```

Removes Python caches only.

### Full artifact reset (destructive)

```bash
make reset
```

Removes pipeline artifacts for Stages 02–05
but **preserves Stage 02 cleaned data**, which is required for schema regeneration.

---

## 8. Folder Structure Overview

```code
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

data/
  stage01_schema/
  stage02_raw/
  stage02_cleaned/
  stage03_intermediate/
  stage04_processed/
  stage05_reports/

configs/
logs/
tests/
docs/
```

---

## 9. Contributing Code

### Formatting

Black + Ruff are enforced:

```bash
make lint
```

### Testing

All new code must include tests:

```bash
make test
```

### Diagnostics

Every stage must include a diagnostics script under:

```code
scripts/diagnostics/<stage>/
```

### Pull Requests

- Include a description of changes
- Include test coverage
- Update diagnostics if needed

---

## 10. Debugging Tips

### VS Code Launchers

Use:

- “Diagnostics: Stage 01 Schema”
- “Run Stage 02 Ingestion”
- “Run Stage 03 Quality”
- “Run Stage 04 Reporting”
- “Run Stage 05 Pipeline Runner”
- “Pytest: Full Workspace”

### Common Issues

- Missing cleaned data → run Stage 02
- Schema mismatch → run Stage 01
- Intermediate artifacts missing → run Stage 03
- Reports missing → run Stage 04
- Pipeline summary missing → run Stage 05

---

## 11. Contact

Maintainer: Brian Deng <br>
Email: <bdeng.data.pipelines@gmail.com> <br>
GitHub: <https://github.com/bdeng1018>
