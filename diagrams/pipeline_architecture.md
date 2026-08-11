# Pipeline Architecture — CMS Data Quality & Ingestion Pipeline

The CMS Data Quality & Ingestion Pipeline is a deterministic, five‑stage system that processes POS/QIES data from raw ingestion to final reporting.

This document provides a visual and structural overview of how the pipeline executes, how artifacts flow between stages, and how diagnostics, logging, and Makefile orchestration integrate into the architecture.

This is the **Branch 1 architecture** (Stages 01–05).

---

## 1. Pipeline Architecture Diagram

```mermaid
flowchart TD
    %% Top-level title
    A0(["🧩 CMS Data Quality & Ingestion Pipeline<br/>Branch 1 — Deterministic Stages 01–05"])

    %% Stage boxes (blue)
    A1["📘 Stage 01 — Schema Definition<br/>• load schema.json<br/>• validate sample rows<br/>• schema diagnostics"]
    A2["📥 Stage 02 — Raw Ingestion<br/>• POS/QIES loaders<br/>• minimal column guarantees<br/>• cleaned canonical dataset"]
    A3["🔍 Stage 03 — Data Quality<br/>• null profiling<br/>• duplicate detection<br/>• drift indicators<br/>• intermediate artifacts"]
    A4["📊 Stage 04 — Reporting<br/>• dataset summary<br/>• column health<br/>• sparse columns<br/>• facility rankings<br/>• manifest"]
    A5["⚙️ Stage 05 — Pipeline Runner<br/>• orchestrates stages 01–04<br/>• config + logging<br/>• pipeline_summary.json"]

    %% Pipeline flow
    A0 --> A1 --> A2 --> A3 --> A4 --> A5

    %% Data artifacts (green)
    subgraph DATA[Data Artifacts]
        D1["🗂️ data/stage01_schema"]
        D2["🗂️ data/stage02_raw<br/>🗂️ data/stage02_cleaned"]
        D3["🗂️ data/stage03_intermediate"]
        D4["🗂️ data/stage04_processed"]
        D5["🗂️ data/stage05_reports"]
    end

    A1 -- writes --> D1
    A2 -- writes --> D2
    A3 -- writes --> D3
    A4 -- writes --> D4
    A5 -- writes --> D5

    %% Diagnostics (yellow)
    subgraph DIAG[Diagnostics Scripts]
        X1["🧪 scripts/diagnostics/stage01"]
        X2["🧪 scripts/diagnostics/stage02"]
        X3["🧪 scripts/diagnostics/stage03"]
        X4["🧪 scripts/diagnostics/stage04"]
        X5["🧪 scripts/diagnostics/stage05"]
    end

    A1 -. checks .-> X1
    A2 -. checks .-> X2
    A3 -. checks .-> X3
    A4 -. checks .-> X4
    A5 -. checks .-> X5

    %% Logging (gray)
    subgraph LOGS[Logging]
        L1["📝 logs/ingestion.log"]
        L2["📝 logs/quality.log"]
        L3["📝 logs/runner.log"]
    end

    A2 -. logs .-> L1
    A3 -. logs .-> L2
    A5 -. logs .-> L3

    %% Makefile targets (purple)
    subgraph MK[Makefile Targets]
        M1["🛠️ make stage01"]
        M2["🛠️ make stage02"]
        M3["🛠️ make stage03"]
        M4["🛠️ make stage04"]
        M5["🛠️ make stage05"]
        M6["🛠️ make run"]
        M7["🛠️ make smoke"]
        M8["🛠️ make diagnostics"]
    end

    MK --> A1

    %% ============================
    %% COLOR CODING
    %% ============================

    %% Stage boxes — light blue
    style A1 fill:#D0E7FF,stroke:#000,color:#000
    style A2 fill:#D0E7FF,stroke:#000,color:#000
    style A3 fill:#D0E7FF,stroke:#000,color:#000
    style A4 fill:#D0E7FF,stroke:#000,color:#000
    style A5 fill:#D0E7FF,stroke:#000,color:#000

    %% Data artifacts — light green
    style D1 fill:#DFFFD6,stroke:#000,color:#000
    style D2 fill:#DFFFD6,stroke:#000,color:#000
    style D3 fill:#DFFFD6,stroke:#000,color:#000
    style D4 fill:#DFFFD6,stroke:#000,color:#000
    style D5 fill:#DFFFD6,stroke:#000,color:#000

    %% Diagnostics — light yellow
    style X1 fill:#FFF7CC,stroke:#000,color:#000
    style X2 fill:#FFF7CC,stroke:#000,color:#000
    style X3 fill:#FFF7CC,stroke:#000,color:#000
    style X4 fill:#FFF7CC,stroke:#000,color:#000
    style X5 fill:#FFF7CC,stroke:#000,color:#000

    %% Logging — light gray
    style L1 fill:#F0F0F0,stroke:#000,color:#000
    style L2 fill:#F0F0F0,stroke:#000,color:#000
    style L3 fill:#F0F0F0,stroke:#000,color:#000

    %% Makefile targets — light purple
    style M1 fill:#E8D9FF,stroke:#000,color:#000
    style M2 fill:#E8D9FF,stroke:#000,color:#000
    style M3 fill:#E8D9FF,stroke:#000,color:#000
    style M4 fill:#E8D9FF,stroke:#000,color:#000
    style M5 fill:#E8D9FF,stroke:#000,color:#000
    style M6 fill:#E8D9FF,stroke:#000,color:#000
    style M7 fill:#E8D9FF,stroke:#000,color:#000
    style M8 fill:#E8D9FF,stroke:#000,color:#000
```

---

## 2. Deterministic Stage Responsibilities

### 📘 Stage 01 — Schema Definition

- Regenerate `schema.json` from cleaned Stage 02 data
- Validate column names, order, and types
- Run schema diagnostics
- Enforce deterministic schema boundaries

**Outputs**

- `data/stage01_schema/schema.json`
- Stage 01 diagnostics

### 📥 Stage 02 — Raw Ingestion

- Fetch POS/QIES raw files
- Ingest parquet/CSV
- Apply minimal column guarantees
- Produce canonical cleaned dataset
- Run ingestion diagnostics

**Outputs**

- `data/stage02_raw/*`
- `data/stage02_cleaned/cleaned_data.csv`

### 🔍 Stage 03 — Data Quality Profiling

- Null profiling
- Duplicate detection
- Drift indicators
- Intermediate artifacts
- Quality diagnostics

**Outputs**

- `data/stage03_intermediate/*`

### 📊 Stage 04 — Reporting

- Dataset summary
- Column health scoring
- Sparse column detection
- Facility ranking reports
- Manifest generation

**Outputs**

- `data/stage04_processed/*`

### ⚙️ Stage 05 — Pipeline Runner

- Orchestrate Stages 01–04
- Load config + logging
- Produce pipeline summary
- Run pipeline diagnostics

**Outputs**

- `data/stage05_reports/pipeline_summary.json`

---

## 3. Artifact Flow

Artifacts move deterministically:

| Stage | Writes |
| ------- | -------- |
| Stage 01 | `data/stage01_schema/` |
| Stage 02 | `data/stage02_raw/`, `data/stage02_cleaned/` |
| Stage 03 | `data/stage03_intermediate/` |
| Stage 04 | `data/stage04_processed/` |
| Stage 05 | `data/stage05_reports/` |

Each artifact directory is isolated and reproducible.

---

## 4. Diagnostics Architecture

Diagnostics run in parallel with pipeline execution:

```code
scripts/diagnostics/stage01
scripts/diagnostics/stage02
scripts/diagnostics/stage03
scripts/diagnostics/stage04
scripts/diagnostics/stage05
```

Run all diagnostics:

```bash
make diagnostics
```

Diagnostics validate:

- input availability
- output correctness
- schema consistency
- artifact completeness
- logical invariants

---

## 5. Logging Architecture

Stage-specific logs:

```code
logs/ingestion.log        # Stage 02
logs/quality.log          # Stage 03
logs/runner.log           # Stage 04
```

Logging is deterministic and scoped per stage.

---

## 6. Makefile Orchestration

Primary developer interface:

```code
make stage01
make stage02
make stage03
make stage04
make stage05
make run
make smoke
make diagnostics
```

Makefile ensures reproducible execution across environments.

---

## 7. C++ Mechanization Integration

The pipeline uses compiled C++ utilities for:

- deterministic schema validation
- deterministic row counting
- ingestion boundary enforcement

These integrate via Python wrappers and Makefile targets.

See:
`docs/MECHANIZATION_CPP.md`

---

## 8. Relationship to ARCHITECTURE.md

- `ARCHITECTURE.md` = full system architecture (pipeline + deployment)
- `PIPELINE_ARCHITECTURE.md` = pipeline‑only architecture (Stages 01–05)

This document is the visual + structural companion to the full architecture spec.

---

## 9. Legend

- **📘 Blue** — Pipeline Stages
- **🗂️ Green** — Data Artifacts
- **🧪 Yellow** — Diagnostics Scripts
- **📝 Gray** — Logging Outputs
- **🛠️ Purple** — Makefile Targets
