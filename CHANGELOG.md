# Changelog

All notable changes to this project will be documented in this file.

The format follows Keep a Changelog and semantic versioning.

---

## [Unreleased](ca://s?q=Show_Unreleased_changes)

### In Progress — Stage 06 (AI Infrastructure Only)

- deterministic embeddings builder
- vector store integration (FAISS)
- retrieval scaffolding
- RAG pipeline built on Stage 03/Stage 04 artifacts
- LLM summarization + anomaly narratives
- agent loop foundation (multi‑step reasoning + tool calling)
- AI‑augmented quality checks
- AI insights artifacts
- Makefile integration (`make stage06`, `make ai`)
- test scaffolding for retrieval + agent behaviors

---

## [1.0.0](ca://s?q=Show_version_1_0_0) — Branch 1 Deterministic Pipeline (Stages 01–05 + Deployment Layer)

### Added — Deterministic Freeze Pipeline

- `bump_version.py` (template population, metadata injection, SBOM counts, digest computation)
- `freeze_runner.py` (canonicalization + detached signature)
- deterministic formatting across manifest, SBOM, provenance
- neutralized hashing for SBOM + provenance integrity block
- docker digest ingestion + artifact wiring
- signature validation (`validate_signature.py`)
- full CI/CD freeze workflow (build → freeze → drift‑check → bundle)
- reproducible release bundles (`cms-pipeline-<VERSION>.tar.gz`)

### Added — Deployment Layer

- deployment contracts (`CONTRACTS.md`, `MANIFEST_SPEC.md`, `SBOM.md`, `VERSIONING.md`)
- provenance validator (`validate_provenance.py`)
- SBOM validator (`validate_sbom.py`)
- audit log generator (`generate_audit_logs.py`)
- drift detection workflow (Terraform + Helm diff)
- governance, compliance, risk, access‑control documentation
- security hardening (`HARDENING.md`)
- incident response playbook (`INCIDENT_RESPONSE.md`)
- deployment orchestrator (`deployment/Makefile.deploy`)
- deterministic Dockerfile + root‑level Compose
- Helm chart + Kubernetes manifests
- Terraform provisioning module
- logging + monitoring stack (Fluent Bit, Prometheus, Grafana)

### Added — Pipeline Infrastructure

- full Makefile rewrite (deterministic PYTHONPATH, directory creation, freeze target)
- Stage 01–05 regeneration workflow
- unified diagnostics (`diagnostics`, `smoke`, `run`)
- deterministic Stage 01–05 artifact structure
- directory‑safe regeneration (mkdir‑p everywhere)

### Changed — Pipeline Integration

- normalized versioning across pipeline + deployment layers
- updated CI workflow (metadata validation, timestamp injection, release bundling)
- improved Makefile targets (`freeze`, `provenance`, `sbom`)
- standardized directory structure for all stages
- improved Stage 03 → Stage 04 consistency checks
- updated root README + deployment README

### Fixed — Determinism + Validation

- SBOM component version mismatches
- manifest semantic‑version validation failures
- provenance integrity block drift
- CI workflow failures due to missing environment variables
- audit log formatting inconsistencies
- drift detection false positives
- Makefile PYTHONPATH inconsistencies
- missing directory creation in Stages 01–05

### Notes

- Branch 1 is now a **complete deterministic + deployable pipeline platform**
- Stage 06 introduces **GenAI + RAG + agentic AI**
- Branch 2 will extend Stage 06 with CI/CD + API integration

---

## [0.2.0](ca://s?q=Show_version_0_2_0) — Branch 1 MVP — Stage 05 Complete

### Added

- Stage 05 pipeline runner
- `pipeline_summary.json`
- Stage 05 validation layer
- multi‑stage diagnostics
- Makefile orchestration (`run`, `smoke`, `diag-intermediate`)
- documentation updates
- unified runner + diagnostics logging

### Changed

- normalized `facility_id` dtype
- improved Stage 03 → Stage 04 consistency checks
- refined Makefile workflow
- updated root README
- standardized intermediate/final artifact structure

### Fixed

- false `facility_id` mismatches
- Stage 05 runner edge cases
- Stage 02 QIES diagnostic invocation errors
- logging inconsistencies

### Notes

- Branch 1 contains a complete deterministic pipeline (Stages 01–05)
- Stage 06 (AI/RAG/Agentic augmentation) begins next

---

## [0.1.0](ca://s?q=Show_version_0_1_0) — Branch 1 MVP — Stages 01–04 Complete

### Added

- Stage 01 schema validation
- Stage 02 raw ingestion
- Stage 03 data‑quality profiling
- Stage 04 reporting layer
- Makefile workflow
- logging system
- full test suite
- diagnostics scripts
- repository structure + environment setup
- pipeline + schema diagrams

### Changed

- updated root README
- improved Makefile reset target
- standardized directory structure
- unified logging configuration

### Fixed

- POS/QIES dtype inconsistencies
- Stage 03 missing‑key behavior
- Stage 04 manifest generation
- facility health classification edge cases

### Notes

- Stage 05 scaffold existed but was not part of v0.1.0
- data directories included for reproducibility
