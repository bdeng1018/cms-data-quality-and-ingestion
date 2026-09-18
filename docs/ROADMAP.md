# Roadmap — CMS Data Quality & Ingestion Pipeline (v1.1.1)

A forward-looking plan for the **cms-data-quality-and-ingestion** deterministic pipeline.
This roadmap outlines the remaining work for **Branch 1**, and the future architecture for **Branch 2** (high‑performance validation, AI harness, semantic enrichment, and inference).

---

## 1. Branch 1 — Deterministic Pipeline (Current)

Branch 1 establishes a fully deterministic ingestion, validation, quality profiling, and reporting pipeline for POS/QIES data.
As of **v1.1.1**, Branch 1 is nearly complete and production‑ready.

### 1.1 Completed

- Stage 01 — Schema Definition
- Stage 02 — Raw Ingestion
- Stage 03 — Data Quality Profiling (v1.1.1 completeness + drift invariants)
- Stage 04 — Reporting (v1.1.1 column health + sparse column contracts)
- Stage 05 — Pipeline Runner (deterministic orchestration + provenance)
- Deterministic C++ mechanization utilities (schema validator + row counter)
- Deployment Layer (CI/CD, Terraform, Logging, Monitoring, Security)
- Documentation (Architecture, Pipeline Flow, Glossary, Style Guide, Stage 03/04/05 Design)

### 1.2 Remaining

- expanded schema drift diagnostics
- sparsity + anomaly diagnostics (Stage 03 extensions)
- additional reporting templates (Stage 04 extensions)
- optional: facility alignment prototype (CCN/NPI)
- optional: enrichment layer stub (future Stage 07)

### 1.3 Goals

- maintain deterministic execution guarantees
- ensure reproducibility across environments
- finalize Branch 1 as a stable ingestion + reporting foundation
- prepare clean boundaries for AI‑driven Branch 2

---

## 2. Branch 2 — Deterministic AI Infrastructure (Future)

Branch 2 introduces deterministic AI components.
These stages do **not** exist yet; this roadmap defines their future boundaries and artifacts.

### 2.1 Stage 06 — High‑Performance Validation + AI Harness (Foundational Only)

Purpose:

- deterministic embeddings (CPU‑safe, reproducible)
- vector store scaffolding
- retrieval logic foundation
- agent loop primitives
- high‑performance validation (parallel row‑count + schema‑check utilities)

Non‑goals:

- no inference
- no generative output
- no model fine‑tuning

Artifacts:

- embedding index
- vector store schema
- retrieval diagnostics
- Stage 06 validation logs

### 2.2 Stage 07 — Enrichment & Semantic Layer

Purpose:

- facility alignment (CCN/NPI)
- provider normalization
- semantic tagging
- metadata augmentation

Artifacts:

- enriched facility dataset
- semantic metadata manifest
- alignment diagnostics

### 2.3 Stage 08 — Inference Layer

Purpose:

- deterministic agent workflows
- retrieval‑augmented inference
- structured output generation

Artifacts:

- inference reports
- agent logs
- retrieval traces
- deterministic inference provenance

---

## 3. Deployment Roadmap

### 3.1 Short‑Term

- expand monitoring dashboards
- add provenance validators
- refine SBOM generation
- improve CI/CD caching and reproducibility

### 3.2 Mid‑Term

- container hardening
- multi‑environment Terraform modules
- optional Helm/K8s deployment

### 3.3 Long‑Term

- inference deployment pipeline
- vector store hosting
- agent orchestration infrastructure

---

## 4. Documentation Roadmap

### 4.1 Completed

- **[ARCHITECTURE.md](ca://s?q=Open_ARCHITECTURE.md)**
- **[PIPELINE_FLOW.md](ca://s?q=Open_PIPELINE_FLOW.md)**
- **[SCHEMA_REFERENCE.md](ca://s?q=Open_SCHEMA_REFERENCE.md)**
- **[STAGE03_DESIGN.md](ca://s?q=Open_STAGE03_DESIGN.md)**
- **[STAGE04_DESIGN.md](ca://s?q=Open_STAGE04_DESIGN.md)**
- **[STAGE05_DESIGN.md](ca://s?q=Open_STAGE05_DESIGN.md)**
- **[STYLE_GUIDE.md](ca://s?q=Open_STYLE_GUIDE.md)**
- **[GLOSSARY.md](ca://s?q=Open_GLOSSARY.md)**

### 4.2 Remaining

- Stage 06 design (when implementation begins)
- Stage 07/08 docs (future)
- AI provenance + retrieval trace specification
- semantic enrichment contract

---

## 5. Guiding Principles

- deterministic execution
- reproducible artifacts
- minimal external dependencies
- clear stage boundaries
- documentation‑first architecture
- deployment‑grade reliability
- audit‑friendly behavior
- future‑proof AI scaffolding

---

## 6. Summary

Branch 1 is nearly complete and provides a stable ingestion + reporting foundation.
Branch 2 will introduce deterministic AI infrastructure, semantic enrichment, and inference stages once implementation begins.

This roadmap ensures the pipeline evolves cleanly, predictably, and with strong architectural discipline.
