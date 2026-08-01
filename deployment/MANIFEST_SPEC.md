# MANIFEST_SPEC.md

CMS Data Quality & Ingestion Pipeline — Manifest Specification

## 1. Purpose

This document defines the formal JSON schema for pipeline run manifests.  
Manifests capture run metadata, environment details, artifact registry references, diagnostics summaries, and provenance information for deterministic, reproducible execution.

All CLI tools, Docker execution, CI/CD workflows, and pipeline runner code must comply with this specification.

---

## 2. Manifest Overview

A manifest is a single JSON file written at the end of each pipeline run.  
It provides:

- run metadata  
- timestamps  
- duration  
- config + environment hashes  
- schema version  
- artifact registry path  
- diagnostics summary  
- provenance information  

Manifests are immutable and versioned.

---

## 3. Manifest File Location

Manifests must be written to:

```code
data/stage05_reports/manifest.json
```

Alternate locations (e.g., versioned manifests) must follow:

```code
data/stage05_reports/manifests/manifest_<run_id>.json
```

---

## 4. Manifest JSON Schema (Formal Specification)

### 4.1 Required Fields

```json
{
  "run_id": "string",
  "timestamp_start": "ISO8601 datetime",
  "timestamp_end": "ISO8601 datetime",
  "duration_seconds": "number",

  "config_path": "string",
  "config_hash": "string",

  "environment_name": "string",
  "environment_hash": "string",

  "schema_version": "string",
  "pipeline_version": "string",

  "artifact_registry_path": "string",
  "artifact_registry_hash": "string",

  "diagnostics_summary": {
      "total_checks": "number",
      "passed": "number",
      "failed": "number",
      "warnings": "number"
  },

  "provenance": {
      "executor": "string",
      "hostname": "string",
      "python_version": "string",
      "os_version": "string",
      "docker_image": "string (optional)"
  }
}
```

---

### 4.2 Optional Fields

```json
{
  "cli_arguments": "object",
  "notes": "string",
  "warnings": ["string"],
  "tags": ["string"],
  "debug": {
      "intermediate_artifacts": ["string"],
      "diagnostic_files": ["string"]
  }
}
```

---

## 5. Field Definitions

### 5.1 `run_id`

A unique identifier for the run.  
Format: `cms_<YYYYMMDD>_<HHMMSS>_<random_suffix>`

### 5.2 `timestamp_start` / `timestamp_end`

ISO8601 timestamps marking the beginning and end of the run.

### 5.3 `duration_seconds`

Floating‑point number representing total runtime.

### 5.4 `config_path` / `config_hash`

The path to the pipeline config file and its SHA‑256 hash.

### 5.5 `environment_name` / `environment_hash`

Name of the environment (local, docker, ci) and a hash of dependency versions.

### 5.6 `schema_version`

Version of the POS/QIES schema used for validation.

### 5.7 `pipeline_version`

Semantic version of the pipeline (MAJOR.MINOR.PATCH).

### 5.8 `artifact_registry_path` / `artifact_registry_hash`

Location and hash of the artifact registry JSON file.

### 5.9 `diagnostics_summary`

Aggregated diagnostic results across all stages.

### 5.10 `provenance`

Execution metadata including:

- executor (CLI, Docker, CI)  
- hostname  
- Python version  
- OS version  
- Docker image (if applicable)

---

## 6. Validation Rules

### 6.1 Required Fields

All required fields must be present.  
Missing fields cause pipeline failure.

### 6.2 Type Validation

Each field must match its declared type.

### 6.3 Hash Validation

- `config_hash` must match the SHA‑256 hash of the config file.  
- `artifact_registry_hash` must match the SHA‑256 hash of the artifact registry.  
- `environment_hash` must match dependency lockfile hash.

### 6.4 Timestamp Validation

`timestamp_end` must be >= `timestamp_start`.

### 6.5 Duration Validation

`duration_seconds` must equal the difference between timestamps.

### 6.6 Diagnostics Validation

`passed + failed + warnings` must equal `total_checks`.

---

## 7. Manifest Versioning

### 7.1 Semantic Versioning

Manifests follow semantic versioning:

- MAJOR — breaking changes  
- MINOR — new fields  
- PATCH — fixes  

### 7.2 Version Field

Manifests must include:

```json
"manifest_version": "MAJOR.MINOR.PATCH"
```

### 7.3 Backward Compatibility

- MINOR and PATCH versions must remain backward compatible.  
- MAJOR versions may introduce breaking changes.

---

## 8. Manifest Generation Rules

### 8.1 When Generated

Manifests are generated at the end of Stage 05.

### 8.2 Atomic Write

Manifests must be written atomically to avoid partial writes.

### 8.3 Deterministic Ordering

JSON keys must be sorted alphabetically.

### 8.4 No Mutation

Manifests must never be overwritten unless versioned.

---

## 9. Example Manifest (Minimal)

```json
{
  "run_id": "cms_20260731_134012_ab12",
  "timestamp_start": "2026-07-31T13:40:12Z",
  "timestamp_end": "2026-07-31T13:40:17Z",
  "duration_seconds": 5.12,

  "config_path": "configs/pipeline.yml",
  "config_hash": "b1c9d4...",

  "environment_name": "docker",
  "environment_hash": "a92f1e...",

  "schema_version": "1.0.0",
  "pipeline_version": "0.3.1",

  "artifact_registry_path": "data/stage05_reports/artifact_registry.json",
  "artifact_registry_hash": "f91c2b...",

  "diagnostics_summary": {
      "total_checks": 42,
      "passed": 42,
      "failed": 0,
      "warnings": 0
  },

  "provenance": {
      "executor": "docker",
      "hostname": "cms-runner",
      "python_version": "3.11.4",
      "os_version": "Ubuntu 22.04",
      "docker_image": "cms_ingestion:0.3.1"
  },

  "manifest_version": "1.0.0"
}
```

---

## 10. Future Extensions

Future manifest fields may include:

- cloud storage URIs  
- pipeline lineage  
- Branch 3 AI/RAG metadata  
- multi‑environment provenance  
- distributed execution metadata  
