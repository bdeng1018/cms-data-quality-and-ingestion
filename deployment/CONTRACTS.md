# CONTRACTS.md

CMS Data Quality & Ingestion Pipeline — Deployment Contracts

## 1. Purpose

This document defines the formal contracts governing deployment, execution, reproducibility, and artifact production for the CMS Data Quality & Ingestion Pipeline (Stages 01–05). These contracts ensure deterministic behavior across local, Docker, and CI/CD environments.

Contracts are binding for:

- schema validation
- ingestion behavior
- artifact production
- manifest structure
- logging format
- diagnostics output
- reproducibility guarantees

All deployment code, CLI tools, Docker images, and CI/CD workflows must comply with these contracts.

---

## 2. Schema Contract

The schema contract defines the rules for validating POS/QIES input data.

### 2.1 Requirements

- Input schema must match `data/stage01_schema/schema.json`.
- All required columns must be present.
- Column types must match the schema definition.
- No additional columns may be introduced without versioning the schema.
- Schema changes require a MINOR or MAJOR version bump.

### 2.2 Enforcement

- `src/stage01_schema_definition/schema_validator.py`
- diagnostics: `scripts/diagnostics/stage01/check_schema.py`

### 2.3 Output

- `column_profiles.json`
- `schema.json` (frozen copy)
- schema version recorded in manifest

---

## 3. Ingestion Contract

The ingestion contract defines how raw POS/QIES data is fetched, cleaned, and written.

### 3.1 Requirements

- Raw data must be written to `data/stage02_raw/`.
- Cleaned data must be written to `data/stage02_cleaned/`.
- No mutation of raw data is allowed.
- Cleaning rules must be deterministic.
- Ingestion errors must be logged and surfaced in diagnostics.

### 3.2 Enforcement

- `src/stage02_raw_ingestion/run_ingestion.py`
- diagnostics: `scripts/diagnostics/stage02/check_ingestion.py`

### 3.3 Output

- `pos_q2_2026.parquet`
- `cleaned_data.csv`
- ingestion metadata in manifest

---

## 4. Artifact Contract

The artifact contract defines the structure, location, and versioning of all pipeline outputs.

### 4.1 Requirements

Artifacts must:

- be written only inside `data/stageXX_*` directories
- include deterministic filenames
- include deterministic content
- include hashes recorded in the artifact registry
- never overwrite previous artifacts unless explicitly versioned

### 4.2 Artifact Types

- schema artifacts (stage01)
- cleaned ingestion artifacts (stage02)
- intermediate quality artifacts (stage03)
- processed reporting artifacts (stage04)
- pipeline summary artifacts (stage05)

### 4.3 Artifact Registry

The artifact registry must include:

- artifact path
- artifact type
- hash
- schema version
- timestamp
- diagnostics status

Registry schema is defined in `MANIFEST_SPEC.md`.

---

## 5. Manifest Contract

The manifest contract defines the JSON schema for run manifests.

### 5.1 Required Fields

- `run_id`
- `timestamp_start`
- `timestamp_end`
- `duration_seconds`
- `config_path`
- `config_hash`
- `environment_hash`
- `schema_version`
- `artifact_registry_path`
- `diagnostics_summary`

### 5.2 Optional Fields

- `warnings`
- `notes`
- `cli_arguments`

### 5.3 Enforcement

- manifest writer in `src/stage05_pipeline_runner`
- CI/CD manifest validation

---

## 6. Logging Contract

The logging contract defines the required format for all logs.

### 6.1 Requirements

Logs must include:

- timestamp
- stage name
- log level
- message
- duration (for stage boundaries)

### 6.2 Log Files

- `logs/ingestion.log`
- `logs/quality.log`
- `logs/runner.log`

### 6.3 Enforcement

- `utils/logging_utils.py`

---

## 7. Diagnostics Contract

Diagnostics validate schema, ingestion, intermediate artifacts, reporting, and pipeline summary.

### 7.1 Requirements

Diagnostics must:

- run deterministically
- produce JSON output
- include pass/fail status
- include remediation hints
- include artifact references

### 7.2 Diagnostic Scripts

Located in:

```code
scripts/diagnostics/stageXX/
```

### 7.3 Output

- diagnostic JSON files
- diagnostic summary in manifest

---

## 8. Reproducibility Contract

The pipeline must produce identical outputs given identical inputs.

### 8.1 Requirements

- deterministic execution
- isolated outputs
- pinned dependencies
- stable schema
- stable manifest schema
- stable artifact registry schema
- stable logging format

### 8.2 Enforcement

- Docker image
- CI/CD pipeline
- CLI execution
- manifest validation
- artifact registry validation

---

## 9. Versioning Contract

Versioning follows semantic versioning:

- MAJOR — breaking contract changes
- MINOR — new features
- PATCH — fixes

Version fields must appear in:

- manifest
- artifact registry
- schema files

---

## 10. Contract Violations

Contract violations must:

- fail the pipeline
- produce diagnostic output
- include remediation hints
- never produce partial artifacts

---

## 11. Future Extensions

Future contract extensions include:

- cloud storage contract
- multi‑environment contract
- Helm deployment contract
- Terraform provisioning contract
- Branch 3 AI/RAG contract hooks
