# 📘 cms-data-quality-and-ingestion — Branch 1 (Deterministic Pipeline)

A lightweight, reproducible, and contract‑driven data‑engineering pipeline for ingesting, validating, profiling, and reporting on large **CMS POS** and **CMS QIES** public datasets.

Branch 1 delivers a **fully deterministic**, multi‑stage workflow (Stages 01–05) with structured artifacts, diagnostics, and deployment guarantees.

---

## 🚀 Overview

Branch 1 implements a clean, testable workflow:

- Stage 01 — schema definition & validation
- Stage 02 — raw ingestion into canonical structures
- Stage 03 — baseline data‑quality profiling
- Stage 04 — structured reporting artifacts
- Stage 05 — deterministic pipeline orchestration

Future branches introduce CCN/NPI alignment, facility enrichment, synthetic claims, and AI/RAG/agentic inference.

See also:

- **[Architecture](ca://s?q=Open_ARCHITECTURE.md)**
- **[Pipeline Flow](ca://s?q=Open_PIPELINE_FLOW.md)**
- **[Data Dictionary](ca://s?q=Open_DATA_DICTIONARY.md)**
- **[Schema Reference](ca://s?q=Open_SCHEMA_REFERENCE.md)**

---

## 📂 Project Structure

```text
cms-data-quality-and-ingestion/
│
├── configs/                 # logging + pipeline configs
├── data/                    # stage01–stage05 artifacts
├── deployment/              # Docker, CI/CD, Terraform, security
├── diagrams/                # architecture + schema diagrams
├── docs/                    # full documentation suite
├── logs/                    # ingestion + quality + runner logs
├── scripts/                 # diagnostics + utilities
├── src/                     # stage01–stage05 pipeline code
├── tests/                   # pytest suites for all stages
├── utils/                   # shared utilities
│
├── Makefile                 # deterministic workflow
├── compose.yml              # deployment runner
├── environment.yml          # conda environment
└── README.md                # project landing page
```

---

## 🏥 Dataset Scope (POS + QIES)

Branch 1 ingests two CMS public datasets:

- **POS** — large, sparse, provider‑type‑specific fields
- **QIES** — smaller, structured facility certification metadata

These datasets are ideal for demonstrating real ingestion, validation, and profiling workflows.

---

## 🔧 Pipeline Features (Stages 01–05)

- deterministic ingestion of POS/QIES
- schema validation + minimal column guarantees
- baseline quality checks (nulls, duplicates, drift, sparsity)
- structured JSON/CSV reporting artifacts
- reproducible Makefile workflow
- deterministic Docker + Compose deployment

---

## 🛠️ Running the Pipeline (Local)

### 1. Create environment (optional)

```bash
make env
conda activate pos_qies_pipeline
```

### 2. Run full pipeline

```bash
make run
```

### 3. Run smoke test

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

### 5. Diagnostics

```bash
make diagnostics
make diag-pos
make diag-qies FILE=/path/to/qies.csv
```

### 6. Tests

```bash
make test
```

### 7. Cleanup

```bash
make clean-cache
```

---

## 🏗 Deployment (Deterministic)

Branch 1 includes a full deterministic deployment subsystem:

- Dockerfile + Compose
- provenance validation
- SBOM validation
- artifact registry
- drift detection
- governance + compliance + access control

Run deployment:

```bash
make deploy
```

Bring down the environment:

```bash
docker compose down
```

---

## 📄 Documentation

Full documentation lives under `docs/`.

---

## 👤 Maintainer

**Brian Deng** <br>
Los Angeles, CA <br>
<bdeng.data.pipelines@gmail.com>

### Focus Areas

- healthcare data engineering
- analytics systems design
- scientific computing
- data quality & governance
- technical writing
