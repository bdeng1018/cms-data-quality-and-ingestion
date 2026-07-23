# 📘 cms-data-quality-and-ingestion (Branch 1 MVP)

A lightweight, reproducible, and scalable data‑engineering pipeline for ingesting, validating, and profiling large CMS public datasets.

Branch 1 (MVP) focuses on **high‑volume ingestion**, **schema‑driven validation**, **baseline data-quality profiling**, and **structured reporting** for CMS POS and QIES before expanding to full provider/facility enrichment.

---

## 🚀 Overview

This repository contains the first milestone of a multi‑stage CMS ingestion and quality pipeline.
Branch 1 establishes a clean, testable workflow that:

- ingests large CMS datasets (POS, QIES)
- validates schema structure (Stage 01)
- loads raw data into canonical structures (Stage 02)
- performs baseline data‑quality checks (Stage 03)
- generates structured reporting artifacts (Stage 04)
- orchestrates full pipeline execution (Stage 05)

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
│   ├── stage02_raw/
│   ├── stage02_cleaned/
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
    ├── file_io.py
    └── logging_utils.py
```

---

## 🏥 Dataset (MVP Scope)

Branch 1 ingests **two** CMS datasets:

### POS (Provider of Services Master File)

- Large, sparse, provider‑type‑specific fields
- Many columns structurally null (expected)

### QIES (Quality Improvement and Evaluation System)

- Smaller, more structured
- Facility certification metadata

These datasets are large, messy, and ideal for demonstrating real ingestion, validation, and quality-profiling workflows.

---

## 🔧 MVP Features

- **Raw ingestion** — load POS/QIES files into canonical DataFrames
- **Schema validation** — enforce structural consistency
- **Minimal column guarantees** — essential fields only
- **Baseline quality checks** - nulls, duplicates, drift indicators
- **Reporting layer** - structured JSON/CSV outputs (Stage 04)
- **Logging + diagnostics** — ingestion, quality, and reporting logs
- **Makefile workflow** — reproducible execution across all stages

This MVP focuses on **ingestion + validation + quality + reporting**, not full transformation.

---

## 🧪 Data Quality Outputs

Stage 03 produces lightweight quality metrics:

- row counts
- null counts
- duplicate counts
- schema drift indicators
- warnings for high-null columns or duplicate keys

Stage 04 transforms these into structured reporting artifacts.

---

## 🛠️ How to Run the Pipeline (MVP)

### 1. Create environment (optional)

```bash
make env
conda activate pos_qies_pipeline
```

### 2. Run full pipeline (Stages 01–05)

```bash
make run
```

### 3. Run smoke test (Stages 02-04)

```bash
make smoke
```

### 4. Run individual stages

```bash
make stage01
make stage02
make stage03
make stage04
make stage05
```

### 5. Run diagnostics

```bash
make diagnostics
make diag-pos
make diag-qies FILE=/path/to/qies.csv
```

### 6. Run tests

```bash
make test
```

### 7. Remove cache

```bash
make clean-cache
```

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
- cleaned canonical dataset

### Stage 03 — Data Quality

- null profiling
- duplicate detection
- drift indicators
- quality logs
- POS Master File sparsity handling
- robust missing-key behavior

### Stage 04 — Reporting

- transforms Stage 03 intermediate artifacts into structured JSON/CSV outputs
- dataset‑level summary
- column‑level health assessment
- sparse column detection
- facility‑level quality scoring
- top/bottom facility rankings
- manifest generation

### Stage 05 — Pipeline Runner

- orchestrates multi‑stage execution
- integrates configs + logging
- produces `pipeline_summary.json`

---

## Branch 1 Status

Branch 1 (Deterministic Pipeline) is nearly complete:

- Stages 01–05 implemented
- Diagrams added (pipeline + schema)
- Diagnostics and Makefile orchestration finalized

Stage 06 is being created to design infrastructure for non-deterministic AI systems.

Branch 2 (AI Inference) will depend on Stage 06.

---

## 📈 Roadmap

- transformation layer (facility normalization, address cleaning)
- validation layer (schema enforcement + integrity checks)
- provider/facility enrichment
- synthetic claims integration
- dashboard + metrics

Stage 06 scaffolding will be added in Branch 1; full AI/RAG/agentic workflows arrive in Branch 2.

---

## 🧭 Notes

This README is intentionally concise — it will evolve as the pipeline grows.
Branch 1 prioritizes **clarity, reproducibility, and correctness** over completeness.

---

## 👤 Author & Maintainer

**Brian Deng** <br>
Los Angeles, CA <br>
<bdeng.data.pipelines@gmail.com>

### Focus Areas

- healthcare data engineering
- analytics systems design
- scientific computing
- data quality & governance
- technical writing
