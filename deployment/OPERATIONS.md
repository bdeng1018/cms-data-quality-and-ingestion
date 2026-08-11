# OPERATIONS.md

CMS Data Quality & Ingestion Pipeline — Operational Specification

## 1. Purpose

This document defines the operational behavior, runtime guarantees, logging rules, diagnostics expectations, error‑handling requirements, and lifecycle management for the CMS Data Quality & Ingestion Pipeline (Stages 01–05).

Operations are deterministic, reproducible, and contract‑driven.
All execution environments (local, Docker, docker‑compose, CI/CD) must comply with this specification.

C++ mechanization (Stage 01 validators + ingestion utilities) is included as a first‑class operational component beginning in v1.1.0.

---

## 2. Operational Principles

Operations follow these principles:

- deterministic execution
- isolated outputs
- reproducible environments
- contract‑driven behavior
- atomic writes
- transparent diagnostics
- zero mutation of source data
- stable logging format
- stable artifact structure
- deterministic C++ mechanization behavior

These principles ensure reliability across ingestion, quality checks, reporting, and pipeline orchestration.

---

## 3. Runtime Lifecycle

### 3.1 Lifecycle Stages

Each pipeline run follows this lifecycle:

1. **Initialization**
   - load config
   - validate config
   - compute config hash
   - initialize logging
   - detect mechanization mode (python-only vs python+cpp)

2. **Environment Validation**
   - validate Python version
   - validate dependency lockfile
   - compute environment hash
   - validate C++ toolchain availability (docker + CI/CD)

3. **Stage Execution**
   - Stage 01: schema validation
     - Python validator
     - C++ schema validator (deterministic mechanization)
   - Stage 02: ingestion + cleaning
     - Python ingestion
     - C++ row counter (raw + cleaned)
   - Stage 03: data quality
   - Stage 04: reporting
   - Stage 05: pipeline runner + summary

4. **Diagnostics**
   - run stage‑specific diagnostics
   - include C++ mechanization diagnostics
   - aggregate diagnostic summary

5. **Artifact Registry Generation**
   - compute artifact hashes
   - write artifact registry
   - include mechanization outputs
   - validate registry schema

6. **Manifest Generation**
   - write manifest
   - include mechanization mode
   - include C++ logs + exit codes
   - validate manifest schema

7. **Completion**
   - finalize logs
   - write duration
   - write provenance
   - write mechanization metadata

---

## 4. Logging Specification

### 4.1 Log Format

Logs must follow this format:

```code
[timestamp] [stage] [level] message
```

### 4.2 Required Fields

- timestamp (ISO8601)
- stage name
- log level (INFO, WARNING, ERROR)
- message
- duration (for stage boundaries)
- C++ mechanization subprocess output (stdout + stderr)

### 4.3 Log Files

Logs must be written to:

```code
logs/ingestion.log
logs/quality.log
logs/runner.log
logs/mechanization.log
```

### 4.4 Determinism

Given identical inputs, logs must be identical except for timestamps.

C++ mechanization logs must be bit‑for‑bit identical across environments.

---

## 5. Diagnostics Specification

### 5.1 Diagnostic Stages

Diagnostics must run for:

- Stage 01: schema
- Stage 02: ingestion
- Stage 03: intermediate artifacts
- Stage 04: reporting
- Stage 05: pipeline summary
- C++ mechanization (validator + row counter)

### 5.2 Diagnostic Output

Diagnostics must produce:

```json
{
  "check_name": "string",
  "status": "pass|fail|warning",
  "details": "string",
  "remediation": "string (optional)"
}
```

### 5.3 Diagnostic Summary

Diagnostics summary must include:

- total checks
- passed
- failed
- warnings
- mechanization checks (C++ validator + row counter)

This summary is written into the manifest.

### 5.4 Determinism

Diagnostics must produce identical results given identical inputs, including mechanization outputs.

---

## 6. Error Handling Specification

### 6.1 Error Types

Errors must be categorized as:

- ingestion errors
- schema errors
- quality errors
- reporting errors
- pipeline orchestration errors
- mechanization errors (C++ validator + row counter)

### 6.2 Error Requirements

Errors must:

- include stage name
- include file + line number
- include remediation hints
- never produce partial artifacts
- never mutate source data
- fail fast
- include C++ exit codes + stderr when mechanization fails

### 6.3 Fatal Errors

Fatal errors must:

- stop pipeline execution
- write diagnostic output
- write partial manifest with error flag
- write logs up to failure point
- include mechanization failure details when applicable

---

## 7. Artifact Isolation

### 7.1 Isolation Rules

Artifacts must:

- be written only inside `data/stageXX_*` directories
- never overwrite previous artifacts unless versioned
- include deterministic filenames
- include deterministic content
- include hashes recorded in the artifact registry
- include mechanization outputs (validator logs, row counter outputs)

### 7.2 Atomic Writes

All artifacts must be written atomically to avoid partial writes.

---

## 8. Environment Guarantees

### 8.1 Python Environment

Environment must include:

- pinned Python version
- pinned dependency versions
- reproducible lockfile (`uv.lock` or `requirements.txt` with hashes)

### 8.2 Docker Environment

Docker environment must:

- install dependencies deterministically
- include CLI entrypoints
- include diagnostics scripts
- mount input/output directories
- include deterministic C++ toolchain (g++, make, cmake, ninja-build)
- include `utils_cpp/` mechanization layer

### 8.3 docker‑compose Environment

Compose execution uses the root‑level `compose.yml` and must:

- mirror CI/CD execution
- enforce read‑only mounts for code/configs
- isolate data + logs
- run the pipeline runner deterministically
- mount `utils_cpp/` read-only for mechanization

### 8.4 CI/CD Environment

CI/CD must:

- run full test suite
- validate manifest schema
- validate artifact registry schema
- build Docker image
- publish release artifacts
- run C++ mechanization tests (`pytest -m cpp_utils`, `cpp_schema`, `cpp_all`)

---

## 9. Provenance Specification

### 9.1 Required Fields

Provenance must include:

- executor (local, docker, compose, ci)
- hostname
- Python version
- OS version
- dependency hash
- Docker image (if applicable)
- mechanization mode (python-only vs python+cpp)
- C++ compiler version (docker + CI/CD)

### 9.2 Determinism

Provenance must be identical across identical environments.

---

## 10. Operational Versioning

### 10.1 Semantic Versioning

Operations follow semantic versioning:

- MAJOR — breaking operational changes
- MINOR — new operational features
- PATCH — fixes

### 10.2 Version Field

Operational version must appear in:

- manifest
- artifact registry
- deployment docs
- mechanization metadata (compiler + binary hash)

---

## 11. Future Extensions

Future operational extensions include:

- cloud storage operations
- distributed execution operations
- multi‑environment operations
- Branch 3 AI/RAG operational hooks
- container orchestration operations (K8s, Helm)
- Stage 06 high-performance C++ validation operations
