# Changelog

All notable changes to this project are documented here.
This project follows **Keep a Changelog** and **semantic versioning**.

---

## [Unreleased](ca://s?q=Show_Unreleased_changes)

### Planned — Stage 06 (High‑Performance Validation Layer)

- expanded C++ mechanization for large‑file validation
- parallel row‑count + schema‑check utilities
- deterministic multi‑file ingestion validator
- hybrid Python/C++ execution path for Stage 01–03
- Makefile integration (`make stage06`)
- extended diagnostics for high‑performance validation
- documentation updates for Stage 06 design

### Planned — AI Infrastructure & Harness (Foundational Only)

- deterministic AI harness for future RAG/agent workflows
- unified interface for embeddings, retrieval, and summarization
- reproducible embedding pipeline (CPU‑safe deterministic mode)
- retrieval scaffolding built on Stage 03/Stage 04 artifacts
- agent harness foundation (tool routing, structured reasoning)
- AI‑ready artifact structure (`ai/` directory)
- Makefile integration (`make ai-harness`)
- pytest scaffolding for AI harness behaviors

### Notes

- No AI inference, RAG logic, or agent loops will be implemented in this cycle
- Stage 06 will focus on **high‑performance validation** and **AI infrastructure only**
- Full AI/RAG/agentic inference arrives in **Branch 2**

---

## [1.1.0](ca://s?q=Show_version_1_1_0) — Deterministic C++ Mechanization Layer

### Added — C++ Mechanization (Stage 01 Utilities)

- C++ schema validator (`cpp_schema_validator.cpp`)
- C++ row‑counter utility (`csv_row_counter.cpp`)
- Python runners for C++ tools (`run_cpp_schema_validator.py`, `run_csv_row_counter.py`)
- new `utils_cpp/` module for compiled deterministic utilities
- Makefile targets for C++ builds (`make cpp-utils`, `make cpp-schema`)
- deterministic C++ output guarantees (stable ordering + stable error codes)

### Added — Diagnostics & Testing

- Stage 01 C++ diagnostics under `scripts/diagnostics/stage01`
- pytest coverage for:
  - C++ schema validator
  - C++ row counter
  - Python/C++ integration layer
- deterministic test fixtures for POS/QIES schema validation

### Changed — Pipeline Integration

- Stage 01 now supports hybrid Python/C++ validation paths
- updated Stage 01 README with mechanization workflow
- improved Makefile orchestration for C++ execution
- standardized artifact naming for C++ outputs

### Fixed — Deterministic Behavior

- resolved nondeterministic ordering in Python schema validator
- fixed row‑count drift for large POS/QIES files
- stabilized subprocess invocation for C++ runners
- corrected error‑code propagation from C++ → Python

### Notes

- v1.1.0 introduces **deterministic C++ mechanization only**
- Stage 06 (high‑performance validation) is planned but not started

---

## [1.0.3](ca://s?q=Show_version_1_0_3) — First Fully Deterministic + CI‑Stable Release

### Added — Deterministic Release Artifacts

- frozen release manifest (`frozen-release-v1.0.3`)
- deterministic SBOM
- deterministic provenance
- bundle packaging (`cms-pipeline-v1.0.3-bundle`)
- SHA256 digests for all artifacts
- Docker image digest for GHCR image
- reproducible validation scripts (clean‑clone reproducibility)

### Changed — CI/CD Stability + Determinism

- repaired workflow triggers (v1.0.1 and v1.0.2 skipped)
- stabilized freeze pipeline execution
- standardized artifact naming + digest extraction
- improved reproducibility guarantees across all validators

### Fixed — Deterministic Drift + Validation

- resolved nondeterministic ordering in freeze outputs
- fixed digest mismatch conditions in CI
- corrected provenance + SBOM canonicalization edge cases
- eliminated drift‑check false positives

### Notes

- v1.0.3 is the **first fully validated, deterministic, CI‑stable release**
- all artifacts are reproducible from a clean clone
- establishes the modern deterministic release model used for future versions

---

## [1.0.2](ca://s?q=Show_version_1_0_2) — Skipped (Invalid Freeze Output)

### Summary

Version **1.0.2** was generated during CI/CD repair work but was **not published** because
the freeze pipeline produced **non‑deterministic artifacts** and failed reproducibility checks.

### Issues

- nondeterministic ordering in freeze outputs
- inconsistent SBOM component hashing
- provenance integrity block drift
- missing Docker digest extraction
- CI workflow instability during freeze stage

### Notes

- superseded by **v1.0.3**, the first fully deterministic + CI‑stable release
- artifacts from v1.0.2 were intentionally discarded

---

## [1.0.1](ca://s?q=Show_version_1_0_1) — Skipped (CI/CD Workflow Failure)

### Summary

Version **1.0.1** was created automatically by the version bump script but was **never published**
because the CI/CD workflow failed before freeze artifacts could be generated.

### Issues

- broken workflow triggers
- missing environment variables in freeze stage
- digest extraction step failing
- incomplete SBOM + provenance generation
- drift‑check not executed

### Notes

- v1.0.1 produced **no valid deterministic artifacts**
- superseded by v1.0.2 (also skipped) and ultimately **v1.0.3**

---

## [1.0.0](ca://s?q=Show_version_1_0_0) — Branch 1 Deterministic Pipeline (Stages 01–05 + Deployment Layer)

### Added — Deterministic Freeze Pipeline

- `bump_version.py` (template population, metadata injection, SBOM counts, digest computation)
- `freeze_runner.py` (canonicalization + detached signature)
- deterministic formatting across manifest, SBOM, provenance
- neutralized hashing for SBOM + provenance integrity block
- Docker digest ingestion + artifact wiring
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

## [0.2.0](ca://s?q=Show_version_0_2_0) — Branch 1 MVP (Stage 05 Complete)

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

## [0.1.0](ca://s?q=Show_version_0_1_0) — Branch 1 MVP (Stages 01–04 Complete)

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
