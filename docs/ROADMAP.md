# Roadmap

A forward-looking plan for the **cms-data-quality-and-ingestion** deterministic pipeline. This roadmap outlines current progress, remaining Branch 1 work, and future Branch 2 AI infrastructure and inference stages.

---

## 1. Branch 1 — Deterministic Pipeline (Current)

Branch 1 establishes a fully deterministic ingestion and reporting pipeline for POS/QIES data. Most components are complete.

### 1.1 Completed

- Stage 01 — Schema Definition  
- Stage 02 — Raw Ingestion  
- Stage 03 — Data Quality  
- Stage 04 — Reporting  
- Stage 05 — Pipeline Runner  
- Deployment Layer (CI/CD, Terraform, Logging, Monitoring, Security)  
- Documentation (Architecture, Onboarding, Glossary, Style Guide, Stage 05 Design)

### 1.2 Remaining

- Additional diagnostics for schema drift and sparsity  
- Expanded reporting templates  
- Optional: facility alignment prototype (CCN/NPI)  
- Optional: enrichment layer stub (future Stage 07)

### 1.3 Goals

- Maintain deterministic execution guarantees  
- Ensure reproducibility across environments  
- Finalize Branch 1 as a stable ingestion + reporting foundation

---

## 2. Branch 2 — AI Infrastructure (Future)

Branch 2 introduces deterministic AI components. These stages do **not** exist yet; this roadmap defines their future boundaries.

### 2.1 Stage 06 — AI Infrastructure (Placeholder)

Purpose:

- deterministic embeddings  
- vector store scaffolding  
- retrieval logic foundation  
- agent loop primitives  

Non-goals:

- no inference  
- no generative output  
- no model fine-tuning  

Artifacts:

- embedding index  
- vector store schema  
- retrieval diagnostics  

### 2.2 Stage 07 — Enrichment & Semantic Layer

Purpose:

- facility alignment  
- provider normalization  
- semantic tagging  
- metadata augmentation  

Artifacts:

- enriched facility dataset  
- semantic metadata manifest  

### 2.3 Stage 08 — Inference Layer

Purpose:

- deterministic agent workflows  
- retrieval-augmented inference  
- structured output generation  

Artifacts:

- inference reports  
- agent logs  
- retrieval traces  

---

## 3. Deployment Roadmap

### 3.1 Short-Term

- expand monitoring dashboards  
- add provenance validators  
- refine SBOM generation  
- improve CI/CD caching and reproducibility  

### 3.2 Mid-Term

- container hardening  
- multi-environment Terraform modules  
- optional Helm/K8s deployment  

### 3.3 Long-Term

- inference deployment pipeline  
- vector store hosting  
- agent orchestration infrastructure  

---

## 4. Documentation Roadmap

### 4.1 Completed

- ARCHITECTURE.md  
- PIPELINE_FLOW.md  
- SCHEMA_REFERENCE.md  
- STAGE05_DESIGN.md  
- STYLE_GUIDE.md  
- GLOSSARY.md  

### 4.2 Remaining

- Stage 06 design (only when implementation begins)  
- Stage 07/08 docs (future)  

---

## 5. Guiding Principles

- deterministic execution  
- reproducible artifacts  
- minimal external dependencies  
- clear stage boundaries  
- documentation-first architecture  
- deployment-grade reliability  

---

## 6. Summary

Branch 1 is nearly complete and provides a stable ingestion and reporting foundation. Branch 2 will introduce deterministic AI infrastructure and inference stages once implementation begins. This roadmap ensures the pipeline evolves cleanly, predictably, and with strong architectural discipline.
