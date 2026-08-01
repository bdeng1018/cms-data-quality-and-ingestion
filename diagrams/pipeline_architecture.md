# Pipeline Architecture

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

## Responsibilities & Outputs (CMS Branch 1)

### 📘 Stage 01 — Schema Definition

**Responsibilities**

- Load and validate `schema.json`
- Check column types and required fields
- Validate sample rows
- Run schema diagnostics

**Outputs**

- `data/stage01_schema/schema.json`
- Stage 01 schema diagnostics report

---

### 📥 Stage 02 — Raw Ingestion (POS/QIES)

**Responsibilities**

- Fetch POS/QIES raw files
- Ingest parquet/CSV into canonical format
- Apply minimal column guarantees
- Clean POS data into unified dataset
- Run ingestion diagnostics

**Outputs**

- `data/stage02_raw/*.parquet`
- `data/stage02_raw/*.csv`
- `data/stage02_cleaned/cleaned_data.csv`
- POS/QIES ingestion diagnostics

---

### 🔍 Stage 03 — Data Quality Profiling

**Responsibilities**

- Null profiling
- Duplicate detection
- Drift indicators
- Generate intermediate artifacts
- Run quality diagnostics

**Outputs**

- `data/stage03_intermediate/*`
- Quality profiling diagnostics
- Drift / null / duplicate summaries

---

### 📊 Stage 04 — Reporting

**Responsibilities**

- Generate dataset summary
- Score column health
- Detect sparse columns
- Produce facility ranking reports
- Build dataset manifest

**Outputs**

- `data/stage04_processed/*`
- Facility ranking reports
- Column health reports
- Dataset manifest

---

### ⚙️ Stage 05 — Pipeline Runner

**Responsibilities**

- Orchestrate Stages 01–04
- Load config + logging
- Produce pipeline‑level summary
- Run pipeline diagnostics

**Outputs**

- `data/stage05_reports/pipeline_summary.json`
- Pipeline diagnostics
- Runner logs

---

### Legend

- **📘 Blue** — Pipeline Stages  
- **🗂️ Green** — Data Artifacts  
- **🧪 Yellow** — Diagnostics Scripts  
- **📝 Gray** — Logging Outputs  
- **🛠️ Purple** — Makefile Targets
