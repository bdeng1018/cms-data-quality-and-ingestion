# 📘 cms-data-quality-and-ingestion (Branch 1 MVP)

A lightweight, reproducible, and scalable data‑engineering pipeline for ingesting, validating, and profiling large CMS public datasets.

Branch 1 (MVP) focuses on **high‑volume ingestion**, **schema‑driven validation**, and **baseline data-quality profiling** for CMS POS and QIES before expanding to full provider/facility enrichment.

---

## 🚀 Overview

This repository contains the first milestone of a multi‑stage CMS ingestion and quality pipeline.
Branch 1 establishes a clean, testable workflow that:

- ingests large CMS datasets (POS, QIES)
- validates schema structure (Stage 01)
- loads raw data into canonical structures (Stage 02)
- performs baseline data‑quality checks (Stage 03)
- prepares intermediate and processed outputs (Stages 04-05)

Future branches will introduce transformation layers, CCN/NPI validation, facility alignment, enrichment logic, and synthetic‑claims integration.

---

## 📂 Project Structure

```text
cms-data-quality-and-ingestion/
│
├── Makefile
├── environment.yml
├── configs/
│   ├── logging.yml
│   └── pipeline.yml
│
├── data/
│   ├── stage01_schema/
│   │   ├── sample_rows.csv
│   │   └── schema.json
│   ├── stage02_raw/
│   ├── stage03_intermediate/
│   ├── stage04_processed/
│   └── stage05_reports/
│
├── diagrams/
│   ├── pipeline_architecture.png
│   └── schema_overview.png
│
├── logs/
│   ├── ingestion.log
│   ├── quality.log
│   └── runner.log
│
├── scripts/
│   └── diagnostics/
│       ├── stage01/
│       ├── stage02/
│       ├── stage03/
│       ├── stage04/
│       └── stage05/
│
├── src/
│   ├── stage01_schema_definition/
│   ├── stage02_raw_ingestion/
│   ├── stage03_data_quality/
│   ├── stage04_reporting/
│   └── stage05_pipeline_runner/
│
├── tests/
│   ├── stage01_schema_definition/
│   ├── stage02_raw_ingestion/
│   ├── stage03_data_quality/
│   ├── stage04_reporting/
│   └── stage05_pipeline_runner/
│
└── utils/
    ├── address_cleaning.py
    ├── ccn_validation.py
    ├── file_io.py
    └── logging_utils.py
```

---

## 🏥 Dataset (MVP Scope)

Branch 1 ingests **two** CMS datasets:

- **POS (Provider of Services Master File)**
  - Note: This file contains hundreds of provider‑type‑specific fields. Many columns are structurally null — this is expected.
- **QIES (Quality Improvement and Evaluation System)**
  - Smaller, more structured, used for facility certification metadata.

These datasets are large, messy, and ideal for demonstrating real ingestion, validation, and quality-profiling workflows.

---

## 🔧 MVP Features

Each item begins with a Guided Link.

- **Raw ingestion** — load POS/QIES files into canonical DataFrames
- **Schema validationn** — enforce structural consistency
- **Minimal column guraantees** — essential fields only
- **Baseline quality checks** - nulls, duplicates, drift indicators
- **Logging + diagnostics** — ingestion + quality logs
- **Makefile workflow** — reproducible execution

This MVP focuses on **ingestion + validation + quality**, not full transformation.

---

## 🧪 Data Quality Outputs

Stage 03 produces lightweight quality metrics:

- row counts
- null counts
- duplicate counts
- schema drift indicators
- warnings for high-null columns or duplicate keys

Future branches will add referential integrity checks, CCN/NPI validation, and facility/provider enrichment.

---

## 🛠️ How to Run the Pipeline (MVP)

### 1. Create environment (optional)

```bash
make env
conda activate pos_qies_pipeline
```

### 2. Run Stage 01 (schema validation)

```bash
make stage01
```

### 3. Run Stage 02 (raw ingestion)

```bash
make stage02
```

### 4. Run Stage 03 (quality profiling)

```bash
make stage03
```

Developer-direct version:

```bash
PYTHONPATH="$(PWD)/src:$(PWD)" python scripts/diagnostics/stage03/check_quality.py \
    --file data/stage02_raw/pos_q2_2026.csv \
    --type pos
```

### 5. Run diagnostics

```bash
make diag-pos
make diag-qies FILE=/path/to/qies.csv
```

### 6. Run tests

```bash
make test
```

### 7. Reset pipeline artifacts

```bash
make reset
```

Commands will evolve as the pipeline expands.

---

## 🧱 Stage Summaries

### Stage 01 — Schema Definition & Validation

- canonical schema (`data/stage01_schema/schema.json`)
- schema loader + validator
- diagnostics + pytest suite

### Stage 02 — Raw Ingestion

- POS/QIES loaders
- minimal column enforcement
- ingestion logs
- DataFrame metadata

### Stage 03 — Data Quality

- null profiling
- duplicate detection
- drift indicators
- quality logs
- POS Master File sparsity handling
- robust missing-key behavior (e.g., missing CCN)

### Stage 04 — Reporting

- intermediate → processed transformations
- quality summaries

### Stage 05 — Pipeline Runner

- orchestrates multi‑stage execution
- integrates configs + logging

---

## 📈 Roadmap

Each item begins with a Guided Link.

- **Transformation layer** — facility type normalization, address cleaning
- **Validation layer** — schema enforcement + integrity checks
- **Provider/facility enrichment** — join POS/QIES with synthetic claims
- **Graph modeling** — attending ↔ rendering relationships
- **Synthetic claims integration**
- **Dashboard + metrics**

---

## 🧭 Notes

This README is intentionally concise — it will evolve as the pipeline grows.
Branch 1 prioritizes **clarity, reproducibility, and correctness** over completeness.

---

## 👤 Author & Maintainer

**Brian Deng** <br>
Los Angeles, CA

### Focus Areas

Each item begins with a Guided Link.

- **Healthcare data engineering** — CMS synthetic claims, POS/QIES ingestion, schema‑driven pipelines
- **Analytics systems design** — reproducible workflows
- **Scientific computing** — stochastic modeling, environmental data pipelines
- **Data quality & governance** — schema enforcement, drift detection
- **Technical writing** — clear documentation, modular patterns
