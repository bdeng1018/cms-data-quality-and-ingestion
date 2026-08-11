# Developer Onboarding — CMS Data Quality & Ingestion Pipeline

Welcome to the CMS Data Quality & Ingestion Pipeline.
This guide provides everything needed to set up your environment, run deterministic pipeline stages, debug issues, and contribute code confidently.

---

## 1. Prerequisites

Install:

- Python 3.11+
- Conda (recommended)
- VS Code
- Git
- (Optional) Docker + Docker Compose for deployment testing

Clone the repository:

```bash
git clone https://github.com/bdeng1018/cms-data-quality-and-ingestion
cd cms-data-quality-and-ingestion
```

---

## 2. VS Code Workspace Setup

Open the workspace file:

```code
cms-data-ingestion.code-workspace
```

This loads:

- `.vscode/settings.json`
- `.vscode/tasks.json`
- `.vscode/launch.json`
- `.vscode/extensions.json`

### Recommended Extensions

Auto-loaded:

- Python + Pylance
- Black
- Ruff
- Pytest
- Rainbow CSV
- YAML Support
- Makefile Tools
- GitLens

These extensions enforce deterministic formatting, linting, and reproducible development behavior.

---

## 3. Environment Setup

Create the environment:

```bash
make env
```

Activate:

```bash
conda activate pos_qies_pipeline
```

Install local dependencies:

```bash
pip install -e .
```

This installs the pipeline as an editable module and ensures deterministic imports.

---

## 4. Running the Pipeline (Stages 01–05)

Each stage is deterministic and isolated.
Run them individually or via the orchestrator.

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

For full pipeline execution:

```bash
make run
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

Diagnostics are deterministic and do not mutate source data.

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

Tests should always run **before** linting to ensure correctness before formatting.

---

## 7. C++ Utilities (Stage 01 + Mechanization Layer)

The pipeline includes deterministic C++ utilities:

- Stage 01 schema validator
- CSV row counter
- mechanization helpers

Build all C++ binaries:

```bash
make cpp-all
```

Run C++ tests via Python wrappers:

```bash
make python-tests
```

Run the row counter manually:

```bash
./src/utils_cpp/csv_row_counter data/stage02_cleaned/cleaned_data.csv
```

---

## 8. Resetting Pipeline Artifacts

### Safe cleanup (recommended)

```bash
make clean-cache
```

Removes Python caches only.

### Full artifact reset (destructive)

```bash
make reset
```

Removes artifacts for Stages 02–05 but **preserves Stage 02 cleaned data**, required for schema regeneration.

---

## 9. Folder Structure Overview

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
deployment/
```

This structure enforces deterministic boundaries and reproducible artifacts.

---

## 10. Contributing Code

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

Every stage must include a diagnostics script:

```code
scripts/diagnostics/<stage>/
```

### Pull Requests

- Describe changes clearly
- Include test coverage
- Update diagnostics if needed
- Maintain deterministic behavior

---

## 11. Debugging Tips

### VS Code Launchers

Use:

- “Diagnostics: Stage 01 Schema”
- “Run Stage 02 Ingestion”
- “Run Stage 03 Quality”
- “Run Stage 04 Reporting”
- “Run Stage 05 Pipeline Runner”
- “Pytest: Full Workspace”

### Common Issues

- Missing cleaned data → **run Stage 02**
- Schema mismatch → **run Stage 01**
- Missing intermediate artifacts → **run Stage 03**
- Missing reports → **run Stage 04**
- Missing pipeline summary → **run Stage 05**

---

## 12. Contact

Maintainer: Brian Deng <br>
Email: <bdeng.data.pipelines@gmail.com> <br>
GitHub: <https://github.com/bdeng1018>
