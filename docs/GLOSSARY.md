# Glossary

A consolidated reference of key terminology used throughout the **cms-data-quality-and-ingestion** deterministic pipeline, deployment layer, and POS data‑engineering workflows.

---

## Canonical Dataset

The cleaned, structurally validated POS dataset produced by Stage 02. It serves as the single source of truth for all downstream stages, including schema generation, quality scoring, reporting, and orchestration.

## Schema Drift

Any mismatch between the expected schema (Stage 01) and the actual structure of incoming POS files. Drift includes missing columns, unexpected columns, renamed fields, or type inconsistencies.

## Sparsity

A high proportion of null or empty values within a column. POS datasets contain many provider‑type‑specific fields that are sparsely populated. Sparsity is measured in Stage 03 and contributes to quality scoring.

## Provenance

End‑to‑end traceability of dataset origin, transformations, validation steps, and pipeline execution metadata. Ensures deterministic, auditable workflows.

## Artifact Registry

Centralized storage for pipeline outputs, including manifests, quality reports, metrics, SBOMs, and deployment artifacts. Supports reproducibility and governance.

## Deterministic Execution

A pipeline guarantee that identical inputs always produce identical outputs. No randomness, nondeterministic ordering, or inference‑based variability.

## Minimal Column Guarantees

A required subset of POS fields enforced during Stage 02 ingestion. These guarantees ensure downstream stability even when CMS source files vary.

## Quality Metrics

Structured indicators produced in Stage 03, including null counts, sparsity rates, duplicate detection, drift indicators, and key‑integrity checks.

## Facility Alignment

A future transformation layer that aligns POS facilities using CCN/NPI identifiers to enable enrichment, deduplication, and cross‑dataset linkage.

## CCN (CMS Certification Number)

A unique identifier assigned to Medicare/Medicaid‑certified facilities. Used for alignment, enrichment, and facility‑level normalization.

## NPI (National Provider Identifier)

A unique identifier for healthcare providers. Used for provider‑level enrichment and future cross‑dataset linkage.

## Drift Indicators

Flags generated when dataset structure or distribution deviates from historical baselines. Used in Stage 03 to detect anomalies in ingestion quality.

## Manifest

A structured JSON document summarizing pipeline outputs, metadata, quality results, and provenance. Generated in Stage 04 and stored in the artifact registry.

## SBOM (Software Bill of Materials)

A complete inventory of software components used in the pipeline. Supports compliance, security, and deterministic deployment.

## Contracts

Formal definitions of expected inputs, outputs, schemas, and behaviors for each pipeline stage. Contracts ensure consistency across deployments and prevent drift.

## Pipeline Runner

The Stage 05 orchestrator responsible for coordinating execution of all pipeline stages, logging, error handling, and summary generation.

## Diagnostics

Scripts and tools used to validate ingestion, schema correctness, quality scoring, and reporting behavior. Located under `scripts/diagnostics/`.

## Enrichment Layer

A future pipeline stage that will add facility metadata, address normalization, CCN/NPI alignment, and synthetic claims integration.

## Stage 06 Infrastructure

AI‑ready scaffolding providing deterministic embeddings, vector storage, retrieval logic, and agent loop foundations for Branch 2 inference.

## Deployment Layer

The operational environment including Docker, CI/CD, governance, compliance, monitoring, logging, security, and infrastructure‑as‑code.

## Observability

Monitoring of pipeline health via metrics, logs, traces, and alerts. Implemented in `deployment/monitoring/`.

## Hardening

Security measures applied to the pipeline and deployment environment, including least privilege, container hardening, policy enforcement, and dependency auditing.

## Incident Response

Operational procedures for handling ingestion failures, data issues, drift events, or security incidents.

---

This glossary expands as the pipeline evolves through Branch 1, Stage 06, and Branch 2 AI inference.
