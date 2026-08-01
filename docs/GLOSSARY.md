# Glossary

A consolidated reference of key terminology used throughout the **cms-data-quality-and-ingestion** deterministic pipeline, deployment layer, and POS/QIES data‑engineering workflows.

---

## Canonical Dataset

A cleaned, structurally validated dataset produced by Stage 02 ingestion. Serves as the single source of truth for downstream quality checks and reporting.

## Schema Drift

Any deviation between the expected schema (Stage 01) and the actual structure of incoming POS/QIES files. Includes missing columns, unexpected columns, or type mismatches.

## Sparsity

High proportion of null or empty values in a column. Common in POS provider‑type‑specific fields. Tracked in Stage 03 quality metrics.

## Provenance

End‑to‑end traceability of dataset origin, transformations, and validation steps. Ensures deterministic, auditable pipeline execution.

## Artifact Registry

Centralized storage for pipeline outputs: manifests, reports, quality metrics, SBOMs, and deployment artifacts.

## Deterministic Execution

Pipeline behavior that is fully reproducible: same inputs → same outputs. No randomness, nondeterministic ordering, or inference‑based variability.

## Minimal Column Guarantees

Essential fields required for POS/QIES ingestion. Enforced in Stage 02 to ensure downstream consistency.

## Quality Metrics

Structured indicators produced in Stage 03: null counts, duplicate counts, drift indicators, sparsity warnings, and key‑integrity checks.

## Facility Alignment

Future transformation layer aligning POS/QIES facilities using CCN/NPI identifiers.

## CCN (CMS Certification Number)

Unique identifier for Medicare/Medicaid‑certified facilities. Used for facility alignment and enrichment.

## NPI (National Provider Identifier)

Unique identifier for healthcare providers. Used for provider‑level enrichment.

## Drift Indicators

Flags generated when dataset structure or distribution deviates from historical baselines.

## Manifest

A structured JSON document summarizing pipeline outputs, metadata, quality results, and provenance. Generated in Stage 04.

## SBOM (Software Bill of Materials)

A complete inventory of software components used in the pipeline. Supports compliance, security, and deterministic deployment.

## Contracts

Formal definitions of expected inputs, outputs, schemas, and behaviors for each pipeline stage. Ensures consistency across deployments.

## Pipeline Runner

Stage 05 orchestrator coordinating execution of all pipeline stages, logging, and summary generation.

## Diagnostics

Scripts and tools used to validate ingestion, schema, quality, and reporting behavior. Located under `scripts/diagnostics/`.

## Enrichment Layer

Future pipeline stage adding facility metadata, address normalization, and synthetic claims integration.

## Stage 06 Infrastructure

AI‑ready scaffolding providing deterministic embeddings, vector storage, retrieval logic, and agent loop foundations.

## Deployment Layer

Full operational environment including Docker, CI/CD, governance, compliance, monitoring, logging, security, and infrastructure‑as‑code.

## Observability

Monitoring of pipeline health via metrics, logs, traces, and alerts. Implemented in `deployment/monitoring/`.

## Hardening

Security measures applied to the pipeline and deployment environment: least privilege, container hardening, policy enforcement.

## Incident Response

Operational procedures for handling failures, data issues, or security events.

---

This glossary will expand as the pipeline evolves through Branch 1, Stage 06, and Branch 2 AI inference.
