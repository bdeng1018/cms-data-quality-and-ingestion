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

## 📦 Release Version (Deterministic Freeze)

**Current Release:** `v1.1.1`

This release includes deterministic ingestion, schema validation, quality profiling, reporting, pipeline orchestration, and full mechanization provenance.

### Frozen Artifacts

All frozen artifacts for **v1.1.1** live under:

- `deployment/releases/v1.1.1.manifest.json`
- `deployment/sbom/sbom-v1.1.1.json`
- `deployment/provenance/provenance-v1.1.1.json`
- `deployment/provenance/provenance-v1.1.1.sig`

See full release notes under **[v1.1.1 docs](ca://s?q=Open_v1_1_1_release_docs)**.

### Provenance Chain

The provenance chain includes:

- mechanization logs
- pipeline summary
- frozen manifest
- frozen SBOM
- frozen provenance
- docker digest
- CI/CD freeze + drift‑check metadata

See:

- **[Manifest Spec](ca://s?q=Open_MANIFEST_SPEC.md)**
- **[Provenance Spec](ca://s?q=Open_provenance_spec)**
- **[SBOM Spec](ca://s?q=Open_SBOM.md)**

---

## 🎯 Scope — What This Pipeline *Does*

Branch 1 provides a fully deterministic, contract‑driven data‑engineering workflow for CMS POS + QIES.
It focuses on **reproducibility**, **diagnostics**, and **artifact‑based validation**, not on ML or analytics.

Core capabilities:

- deterministic ingestion of CMS POS + QIES
- schema validation with pinned mechanization (C++ Stage 01)
- reproducible cleaning + canonicalization (Stage 02)
- baseline quality profiling (Stage 03)
- structured reporting artifacts (Stage 04)
- deterministic pipeline orchestration (Stage 05)
- full provenance chain + SBOM + manifest validation
- deterministic CI/CD freeze + drift‑check
- deterministic Docker + Compose + Helm deployment
- deterministic Terraform provisioning

See:

- **[Pipeline Flow](ca://s?q=Open_PIPELINE_FLOW.md)**
- **[Stage01 Design](ca://s?q=Open_STAGE01_DESIGN.md)**
- **[Stage03 Design](ca://s?q=Open_STAGE03_DESIGN.md)**
- **[Stage05 Design](ca://s?q=Open_STAGE05_DESIGN.md)**

---

## 🚫 Non‑Scope — What This Pipeline *Does NOT Do*

Branch 1 intentionally avoids higher‑level analytics and domain enrichment.
This keeps the pipeline deterministic and reproducible.

It does **NOT**:

- perform CCN/NPI alignment (Branch 2)
- perform facility enrichment or cross‑dataset joins
- perform claims analytics or synthetic claims generation
- perform ML, forecasting, or anomaly detection
- perform RAG/agentic inference (future branches)
- mutate source data beyond deterministic cleaning
- provide dashboards or BI tooling
- ingest non‑CMS datasets
- run distributed ingestion or autoscaling (future Terraform modules)

See roadmap: **[ROADMAP.md](ca://s?q=Open_ROADMAP.md)**

---

## 📊 Operational Metrics & Results (v1.1.1)

Branch 1 produces deterministic, human‑readable metrics across Stage 03, Stage 04, Stage 05, and the v1.1.1 release artifacts.
All values below come directly from the frozen v1.1.1 pipeline outputs.

### **Quality Metrics (Stage 03)**

**Dataset Quality**

- **Overall quality score:** 0.1521687529 → **15.2%**
- **Completeness:** 15.2% (84.8% missingness)

**Column Metrics**

- **Total columns:** 474
- **Fully missing columns:** dozens (null_count = 44,707)
- **Highly sparse columns:** dozens (null_count ≈ 31k–33k → 70–75% missing)
- **Moderately sparse columns:** some (null_count ≈ 18k → ~40% missing)
- **Fully complete columns:** a few (null_count = 0)

**Column Health (Stage 03)**

- **quality_score = 0.0** → fully missing
- **quality_score ≈ 0.27–0.35** → partially populated
- **quality_score ≈ 0.59** → moderately healthy
- **quality_score ≈ 0.9999** → fully healthy

**Facility Metrics**

- **Total facilities:** 44,707
- **Typical facility missingness:** 93–94% → **6–7% completeness**
- **Best facilities:** ~65% missing → **35% completeness**

Artifacts:

- `column_profiles.json`
- `facility_metrics.csv`
- `quality_summary.json`

See: **[Quality Checks](ca://s?q=Open_check_quality.md)**

### **Reporting Metrics (Stage 04)**

**Dataset Summary**

- **Rows:** 44,707
- **Facilities:** 44,707
- **Columns:** 474
- **Dataset completeness (Stage 04):** 1.0 (all reporting artifacts generated)
- **Dataset quality:** 15.2%
- **Warnings:** none

**Column Health (Stage 04)**

- **Healthy:** 474
- **Moderate:** 0
- **Sparse:** 0
- **Critical:** 0
- Notes: dtype inconsistencies and zero‑distinct‑value columns exist but do not violate contracts.

**Sparse Columns**

- `sparse_columns.json` → **[]**
  (No columns violate Stage 04 sparsity contract.)

**Top Facilities (Highest Completeness)**

- **37.55% completeness:** 260197, 360039, 450099, 260065, 100015, 370028
- **37.34% completeness:** multiple facilities (e.g., 150038, 190175, 370114)

**Bottom Facilities (Lowest Completeness)**

- **5.49% completeness:** 751018, 661802, 391950, 751953, 034656
- **5.91% completeness:** multiple facilities (e.g., 054667, 234631, 164607)

Artifacts:

- `dataset_summary.json`
- `top_facilities.csv`
- `bottom_facilities.csv`
- `sparse_columns.json`
- `column_health.json`

See: **[Reporting Engine](ca://s?q=Open_report_engine.md)**

### **Pipeline Metrics (Stage 05)**

**Execution**

- **Start:** 2026‑09‑17T20:21:52.134860
- **End:** 2026‑09‑17T20:25:12.957663
- **Total runtime:** **200.82 seconds** (3 minutes 20.82 seconds)

**Stage Status**

- Stage 01: success
- Stage 02: success
- Stage 03: success
- Stage 04: success
- Mechanization: success

**Mechanization Provenance**

- Mode: **python+cpp**
- Schema validator: **VALID**
- Ingestion utils: normalize=OK, delimiter=",", BOM=OK
- Exit codes: all **0**

**Ingestion Metrics**

- POS ingestion shape: **44,707 × 474**

**Warnings**

- None

Artifact:

- `pipeline_summary.json`

See: **[Pipeline Runner](ca://s?q=Open_run_pipeline.md)**

### **Release Metadata (v1.1.1)**

**Manifest**

- Version: **v1.1.1**
- Artifacts: docker image, manifest, provenance, SBOM
- Validation: **pending** (expected for local deterministic builds)

**SBOM**

- **Component count:** 4
- **Dependency count:** 3
- Components include:
  - python‑3.11‑slim
  - cms‑pipeline (v1.1.1)
  - docker image (v1.1.1)
  - python dependencies (pandas, pyyaml, pytest)

**Provenance**

- Mode: **deterministic**
- Spec: **slsa‑1.0**
- OS: ubuntu‑22.04
- Integrity: pending (expected for local builds)

Artifacts:

- `v1.1.1.manifest.json`
- `sbom-v1.1.1.json`
- `provenance-v1.1.1.json`

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

See full deployment documentation under:

- **[DEPLOYMENT.md](ca://s?q=Open_DEPLOYMENT.md)**
- **[VERSIONING.md](ca://s?q=Open_VERSIONING.md)**
- **[RELEASE_NOTES.md](ca://s?q=Open_RELEASE_NOTES.md)**
- **[ACCESS_CONTROL.md](ca://s?q=Open_ACCESS_CONTROL.md)**
- **[INCIDENT_RESPONSE.md](ca://s?q=Open_INCIDENT_RESPONSE.md)**
- **[GOVERNANCE.md](ca://s?q=Open_GOVERNANCE.md)**
- **[COMPLIANCE.md](ca://s?q=Open_COMPLIANCE.md)**
- **[RISK_MODEL.md](ca://s?q=Open_RISK_MODEL.md)**
- **[SBOM.md](ca://s?q=Open_SBOM.md)**

---

## 📄 Documentation

Full documentation lives under `docs/`.

---

## 👤 Maintainer

**Brian Deng**  <br>
Los Angeles, CA  <br>
<bdeng.data.pipelines@gmail.com>

### Focus Areas

- healthcare data engineering
- analytics systems design
- scientific computing
- data quality & governance
- technical writing
