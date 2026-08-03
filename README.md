# 📘 cms-data-quality-and-ingestion — Branch 1 (Deterministic Pipeline)

A lightweight, reproducible, and scalable data‑engineering pipeline for ingesting, validating, profiling, and reporting on large **CMS POS** and **CMS QIES** public datasets.
Branch 1 delivers a **fully deterministic**, **contract‑driven**, multi‑stage workflow (Stages 01–05) with structured artifacts, diagnostics, and deployment guarantees.

---

## 🚀 Overview

Branch 1 implements a clean, testable workflow that:

- ingests large CMS datasets (POS, QIES)
- validates schema structure (Stage 01)
- loads raw data into canonical structures (Stage 02)
- performs baseline data‑quality checks (Stage 03)
- generates structured reporting artifacts (Stage 04)
- orchestrates full pipeline execution (Stage 05)

Future branches introduce transformation layers, CCN/NPI alignment, facility enrichment, synthetic claims, and AI/RAG/agentic inference.

---

## 📂 Project Structure

```text
cms-data-quality-and-ingestion/
│
├── Makefile
├── compose.yml
├── environment.yml
│
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
├── deployment/
│   ├── Dockerfile
│   ├── Makefile.deploy
│   ├── DEPLOYMENT.md
│   ├── OPERATIONS.md
│   ├── CONTRACTS.md
│   ├── MANIFEST_SPEC.md
│   ├── SBOM.md
│   ├── VERSIONING.md
│   ├── GOVERNANCE.md
│   ├── COMPLIANCE.md
│   ├── ACCESS_CONTROL.md
│   ├── helm/
│   ├── k8s/
│   ├── terraform/
│   ├── logging/
│   ├── monitoring/
│   └── security/
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
└── utils/
    ├── file_io.py
    └── logging_utils.py
```

---

## 🏥 Dataset Scope (POS + QIES)

Branch 1 ingests **two** CMS public datasets:

### POS (Provider of Services Master File)

- Large, sparse, provider‑type‑specific fields
- Structurally null columns (expected)

### QIES (Quality Improvement and Evaluation System)

- Smaller, more structured
- Facility certification metadata

These datasets are ideal for demonstrating real ingestion, validation, and profiling workflows.

---

## 🔧 Pipeline Features (Stages 01–05)

- **Raw ingestion** — load POS/QIES files into canonical DataFrames
- **Schema validation** — enforce structural consistency
- **Minimal column guarantees** — essential fields only
- **Baseline quality checks** - nulls, duplicates, drift indicators
- **Reporting layer** - structured JSON/CSV outputs (Stage 04)
- **Logging + diagnostics** — ingestion, quality, and reporting logs
- **Makefile workflow** — reproducible execution across all stages
- **Deterministic deployment** — Docker + Compose + CI/CD parity

This MVP focuses on **ingestion + validation + quality + reporting**, not full transformation.

---

## 🧪 Data Quality Outputs

Stage 03 produces lightweight quality metrics:

- row counts
- null counts
- duplicate counts
- schema drift indicators
- sparsity warnings
- missing-key behavior

Stage 04 transforms these into structured reporting artifacts.

---

## 🛠️ Running the Pipeline (Local)

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

### 7. Cleanup: remove cache

```bash
make clean-cache
```

---

## 🏗 Deployment Layer (Deterministic)

Branch 1 includes a full deterministic deployment subsystem:

- Dockerfile (`deployment/Dockerfile`)  
- root‑level Compose (`compose.yml`)  
- deployment orchestrator (`deployment/Makefile.deplo`y)  
- provenance validation  
- SBOM validation  
- artifact registry  
- drift detection  
- governance + compliance + access control  
- operational playbooks  

### Run full deployment (Docker + Compose)

```bash
make deploy
```

This performs:

- deterministic Docker build  
- deterministic Compose execution  
- manifest validation  
- artifact registry validation  

### Bring down the Compose environment

```bash
docker compose down
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

## 🏗 Deployment Layer (Branch 1)

Branch 1 includes a full deployment specification:

- deterministic Docker image
- CI/CD pipeline
- provenance validation
- SBOM validation
- artifact registry
- drift detection
- governance + compliance
- security hardening
- operational playbooks

Deployment documentation lives under `deployment/`.

---

## 🔮 Stage 06 Preview (AI Infrastructure Only)

Stage 06 introduces **AI infrastructure only** (no inference):

- deterministic embeddings
- vector store
- retrieval scaffolding
- agent loop foundation
- AI‑augmented quality checks
- future API‑ready insights

Full AI/RAG/agentic inference arrives in **Branch 2**.

---

## 📈 Roadmap

- transformation + enrichment
- CCN/NPI alignment
- facility normalization
- synthetic claims
- dashboard + metrics
- Stage 06 AI infrastructure
- Branch 2 AI inference

---

## 🧭 Notes

This README is intentionally concise — it will evolve as the pipeline grows.
Branch 1 prioritizes **clarity, reproducibility, and correctness** over completeness.

### Branch 1 Status

Branch 1 (Deterministic Pipeline) is nearly complete:

- Stages 01–05 implemented
- diagnostics + Makefile orchestration finalized
- pipeline + schema diagrams added
- full deployment subsystem added (provenance, SBOM, drift, governance, compliance, access control)

Stage 06 scaffolding is in progress.
Branch 2 (AI inference) will build on Stage 06.

---

## 👤 Author & Maintainer

**Brian Deng**  
Los Angeles, CA  
<bdeng.data.pipelines@gmail.com>

### Focus Areas

- healthcare data engineering
- analytics systems design
- scientific computing
- data quality & governance
- technical writing
