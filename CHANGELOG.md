# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and semantic versioning.

---

## [Unreleased]

### In Progress — Stage 06 (AI Infrastructure only — Deterministic Embeddings, Vector Store, Retrieval Scaffolding)

- AI orchestration layer integrating embeddings, retrieval, and LLM reasoning
- RAG pipeline built on Stage 03/Stage 04 artifacts for facility‑level semantic search
- Embeddings builder for column profiles, facility metrics, and dataset summaries
- Vector store integration using FAISS for low‑latency retrieval
- LLM summarization generating narrative insights and anomaly explanations
- Agent loop implementing multi‑step reasoning and tool/function calling
- AI‑augmented quality checks validating anomalies and missingness patterns
- AI insights artifacts for downstream apps, dashboards, and APIs
- Makefile integration for Stage 06 execution (`make stage06`, `make ai`)
- Test suite scaffolding for agent behaviors, retrieval correctness, and LLM output validation

### Planned — Stage 06: AI Infrastructure Layer (GenAI, RAG, Agentic AI)

Stage 06 introduces an intelligent infrastructure layer on top of the deterministic pipeline (Stages 01–05). This release will add infrastructure (but **not** inference) for **LLM‑powered reasoning**, **retrieval‑augmented generation**, and **agentic workflows** that transform the pipeline from a data processor into a **production‑ready AI system**.

### Scope

- AI Orchestration — unified controller for embeddings, retrieval, LLM reasoning, and agent loops
- RAG Engine — retrieval over Stage 03/Stage 04 artifacts using vector search
- Embeddings Pipeline — facility‑level, column‑level, and report‑level embeddings
- Vector Store — FAISS‑based local index for fast semantic search
- LLM Summarization — narrative facility summaries, anomaly explanations, dataset insights
- Agent Loop — autonomous multi‑step reasoning over metrics, profiles, and reports
- AI‑Augmented Quality Checks — LLM validation of anomalies, missingness patterns, and outliers
- AI Insights Artifacts — JSON outputs for downstream apps, dashboards, and APIs

### Design Goals

- Production‑grade agent workflows (Claude‑compatible function calling + tool use)
- Deterministic + LLM hybrid architecture (pipeline remains reproducible; AI adds intelligence)
- Composable RAG stack (embeddings → vector store → retrieval → LLM reasoning)
- Low‑latency inference paths for facility‑level insights
- Modular AI components isolated in `src/stage06_ai/`
- Testable agent behaviors (mocked LLM responses, deterministic retrieval tests)
- API‑ready outputs for future deployment in Branch 2

### Implementation Plan

- Build embeddings + vector store from Stage 03/Stage 04 artifacts
- Implement retrieval pipelines for facility‑level and dataset‑level context
- Add LLM summarizers for narrative reporting
- Implement agent loop with multi‑step reasoning and tool calls
- Generate AI‑augmented artifacts (`ai_facility_summary.json`, `ai_dataset_insights.json`)
- Add Stage 06 diagnostics + test suite
- Integrate Stage 06 into Makefile (`make stage06`, `make ai`)

### Notes

- Stage 06 is the first release introducing **GenAI**, **RAG**, and **agentic AI**
- This upgrade transforms Branch 1 into a **full‑stack intelligent pipeline**
- Branch 2 will extend Stage 06 with **CI/CD**, **deployment**, and **API integration**

---

## [0.2.0] —  Branch 1 MVP — Stage 05 Complete

### Added

- Stage 05 pipeline runner coordinating Stages 01–04 into a single deterministic workflow
- Pipeline summary artifact (`pipeline_summary.json`) capturing timestamps, stage statuses, warnings, and duration
- Stage 05 validation layer ensuring Stage 04 artifacts (facility reports, dataset summaries, manifests) are complete and consistent
- Multi‑stage diagnostics verifying Stage 02 → Stage 03 → Stage 04 continuity
- Makefile orchestration targets (`run`, `smoke`, `diag-intermediate`) for full pipeline execution
- Documentation updates covering Stage 05 usage, outputs, and integration points
- Unified logging for runner + diagnostics for consistent observability across stages

### Changed

- Normalized `facility_id` dtype across Stage 03 and Stage 05 diagnostics to eliminate false mismatches
- Improved Stage 03 → Stage 04 consistency checks for column profiles, facility metrics, and reporting artifacts
- Refined Makefile workflow to support full‑pipeline execution and developer ergonomics
- Updated root README to reflect Stage 05 completion and new orchestration capabilities
- Standardized directory structure for intermediate and final artifacts

### Fixed

- False `facility_id` mismatches caused by mixed integer/string types in Stage 03 diagnostics
- Stage 05 runner edge cases (missing artifacts, invalid paths, inconsistent manifests)
- Makefile diagnostic invocation errors for Stage 02 QIES ingestion
- Minor logging inconsistencies across ingestion, profiling, and reporting layers

### Notes

- Branch 1 now contains a complete deterministic pipeline (Stages 01–05)
- Stage 06 (AI/RAG/Agentic augmentation) will be introduced in the next release
- Stage 05 establishes the orchestration foundation required for intelligent workflows in Stage 06

---

## [0.1.0] —  Branch 1 MVP — Stages 01–04 Complete

### Added

- Stage 01 — Schema Definition & Validation  
- Stage 02 — Raw Ingestion  
- Stage 03 — Data Quality Profiling  
- Stage 04 — Reporting Layer  
- Makefile workflow (stage01–stage04, reset, diagnostics, tests)  
- Logging system (ingestion, quality, runner)  
- Full test suite across all stages  
- Diagnostics scripts for each stage  
- Repository structure and environment setup  
- Diagrams for pipeline architecture and schema overview

### Changed

- Updated root README to include Stage 04  
- Improved Makefile reset target  
- Standardized directory structure  
- Unified logging configuration

### Fixed

- POS/QIES dtype inconsistencies  
- Stage 03 missing-key behavior  
- Stage 04 manifest generation  
- Facility health classification edge cases

### Notes

- Stage 05 scaffold exists but is not part of v0.1.0  
- Data directories included for reproducibility  
