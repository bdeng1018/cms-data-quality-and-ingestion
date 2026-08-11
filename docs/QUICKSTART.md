# Developer Quickstart

## Overview

A fast, minimal guide for developers working with the CMS Data Quality & Ingestion Pipeline.

This document covers installation, environment setup, running stages, diagnostics, testing, and C++ utilities.

---

## 1. Install & Clone

```bash
git clone https://github.com/bdeng1018/cms-data-quality-and-ingestion
cd cms-data-quality-and-ingestion
make env
conda activate pos_qies_pipeline
pip install -e .
```

---

## 2. Run the Pipeline

Run individual stages:

```bash
make stage02   # ingestion + cleaning
make stage01   # schema definition
make stage03   # quality profiling
make stage04   # reporting
make stage05   # orchestrator
```

Run full pipeline:

```bash
make run
```

---

## 3. Run Diagnostics

All diagnostics:

```bash
make diagnostics
```

Individual diagnostics:

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

## 4. Run Tests & Lint

```bash
make test
make lint
```

Tests should run **before** linting.

---

## 5. Build & Run C++ Utilities

Build all C++ binaries:

```bash
make cpp-all
```

Run row counter:

```bash
./src/utils_cpp/csv_row_counter data/stage02_cleaned/cleaned_data.csv
```

Run schema validator:

```bash
./src/stage01_schema_definition/cpp_schema_validator \
    data/stage01_schema/schema.txt \
    data/stage02_cleaned/cleaned_data.csv
```

---

## 6. Reset Artifacts

Safe cleanup:

```bash
make clean-cache
```

Full reset (destructive):

```bash
make reset
```

Stage 02 cleaned data is preserved.

---

## 7. Common Issues

- Missing cleaned data → run Stage 02
- Schema mismatch → run Stage 01
- Missing intermediate artifacts → run Stage 03
- Missing reports → run Stage 04
- Missing pipeline summary → run Stage 05

---

## 8. VS Code Launchers

Use built-in launchers:

- Diagnostics: Stage 01
- Run Stage 02 Ingestion
- Run Stage 03 Quality
- Run Stage 04 Reporting
- Run Stage 05 Orchestrator
- Pytest: Full Workspace

---

## 9. Contact

Maintainer: Brian Deng <br>
Email: <bdeng.data.pipelines@gmail.com> <br>
GitHub: <https://github.com/bdeng1018>
