# CMS Data Quality & Ingestion Pipeline — Deployment Specification

## 1. Overview

This document defines the deployment architecture, environment guarantees,
execution pathways, and operational expectations for the CMS Data Quality &
Ingestion Pipeline (Stages 01–05). Deployment is contract‑driven and designed for
deterministic, reproducible, and isolated execution across local, Docker,
docker‑compose, and CI/CD environments.

Guiding principles:

- deterministic execution
- reproducible environments
- isolated artifacts
- versioned manifests
- contract‑driven orchestration
- zero mutation of source data
- transparent diagnostics

---

## 2. Deployment Architecture

Deployment consists of four layers:

### 2.1 Execution Layer

- CLI (`cms run`, `cms report`, `cms diagnose`, `cms manifest`)
- Makefile targets (root Makefile + deployment/Makefile.deploy)
- Python entrypoints
- C++ mechanization binaries (Stage 01 validators + ingestion utilities) *deterministically compiled inside Docker; invoked by Python subprocess*

### 2.2 Environment Layer

- Docker image (`deployment/Dockerfile`)
- pinned Python dependencies
- reproducible runtime
- deterministic C++ toolchain (g++, make, cmake, ninja-build) *installed inside Docker for Stage 01 mechanization*

### 2.3 Orchestration Layer

- docker‑compose (`compose.yml` at repository root)
- pipeline runner
- manifest writer
- artifact registry
- provenance tracker
- read‑only mount of `utils_cpp/` for deterministic C++ execution

### 2.4 Validation Layer

- diagnostics scripts
- schema validation
- quality checks
- reporting checks
- C++ schema validator + C++ row counter (Stage 01 mechanization)

Each layer is deterministic and contract‑driven.

---

## 3. Supported Execution Modes

### 3.1 Local Development

Local execution uses:

- CLI commands
- Makefile targets
- local logs + artifacts
- reproducible Python environment
- local C++ builds via `make cpp-utils`, `make cpp-schema`, `make cpp-all`

Local runs must produce identical manifests, artifacts, and diagnostics given
identical inputs.

### 3.2 Dockerized Execution

Docker execution provides:

- reproducible environment
- pinned Python + OS dependencies
- isolated filesystem
- deterministic logs
- deterministic C++ mechanization compiled inside the image

Docker runs must produce bit‑for‑bit identical artifacts to local runs.

### 3.3 docker‑compose Execution

Compose execution uses the root‑level `compose.yml`:

```bash
docker compose up --build
```

Compose provides:

- deterministic mounts
- read‑only code/configs
- isolated data/logs
- CI/CD‑mirrored execution
- read-only mount of C++ mechanization layer (`utils_cpp/`)

### 3.4 CI/CD Execution

CI/CD runs:

- linting
- tests
- Docker build
- manifest validation
- artifact registry validation
- release artifact publishing
- C++ mechanization tests (`pytest -m cpp_utils`, `cpp_schema`, `cpp_all`)

CI/CD must guarantee:

- no mutation of source data
- isolated outputs
- reproducible manifests
- reproducible diagnostics

---

## 4. Deployment Components

### 4.1 CLI Tools

The CLI provides:

- `cms run` — full pipeline execution
- `cms report` — reporting layer
- `cms diagnose` — diagnostics
- `cms manifest` — manifest inspection

CLI commands must:

- accept config paths
- validate arguments
- write manifests
- write provenance
- write artifact registry
- invoke C++ mechanization binaries when configured

### 4.2 Docker Image

The Docker image must:

- pin Python version
- install dependencies deterministically
- include CLI entrypoints
- include diagnostics scripts
- mount input/output directories
- install deterministic C++ toolchain (g++, make, cmake, ninja-build)
- copy `utils_cpp/` into the image for Stage 01 mechanization

### 4.3 docker‑compose

Compose orchestrates deterministic local execution using:

```code
compose.yml
```

Compose must:

- mirror CI/CD execution
- enforce read‑only mounts for code/configs
- isolate data + logs
- run the pipeline runner deterministically
- mount C++ mechanization layer read-only (`utils_cpp:/app/utils_cpp:ro`)

### 4.4 CI/CD Pipeline

CI/CD must:

- run full test suite
- lint code
- build Docker image
- validate manifest schema
- validate artifact registry
- publish release artifacts
- run C++ mechanization tests

Release artifacts include:

- Docker image
- manifest schema
- artifact registry schema
- deployment diagrams

### 4.5 Manifests

Manifests must include:

- run metadata
- timestamps
- duration
- config hash
- environment hash
- artifact index
- diagnostics summary
- mechanization mode (Python-only vs Python + CPP)

Manifest schema is defined in `MANIFEST_SPEC.md`.

### 4.6 Artifact Registry

The artifact registry must:

- list all produced artifacts
- include paths + hashes
- include schema versions
- include diagnostics status
- include C++ mechanization outputs (schema validator logs, row counter outputs)

Artifact registry schema is defined in `CONTRACTS.md`.

---

## 5. Reproducibility Guarantees

Deployment must guarantee:

- deterministic execution
- isolated outputs
- no mutation of source data
- stable schema contracts
- stable manifest schema
- stable artifact registry schema
- stable logging format
- deterministic C++ binary behavior across environments

Given identical inputs, two runs must produce:

- identical manifests
- identical artifacts
- identical diagnostics
- identical C++ mechanization outputs

---

## 6. Operational Expectations

### 6.1 Logging

Logs must include:

- timestamps
- stage boundaries
- warnings
- errors
- duration metrics
- C++ mechanization subprocess logs

### 6.2 Diagnostics

Diagnostics must validate:

- schema
- ingestion
- intermediate artifacts
- reporting artifacts
- pipeline summary
- C++ schema validator results
- C++ row counter results

### 6.3 Error Handling

Errors must:

- be deterministic
- include stage + file + line
- include remediation hints
- never produce partial artifacts
- include C++ mechanization error codes + stderr output

---

## 7. Deployment Directory Structure

```text
deployment/
    DEPLOYMENT.md
    CONTRACTS.md
    MANIFEST_SPEC.md
    OPERATIONS.md
    Dockerfile
    Makefile.deploy
    ci/
    env/
    helm/
    k8s/
    terraform/
    logging/
    monitoring/
    security/
utils_cpp/
```

Note: `compose.yml` lives at the repository root, not inside `deployment/`.

---

## 8. Versioning

Deployment follows semantic versioning:

- MAJOR — breaking contract changes
- MINOR — new features
- PATCH — fixes

Manifests and artifact registries include version fields.

---

## 9. Future Extensions

Future deployment extensions include:

- Helm chart
- Terraform provisioning
- multi‑environment support
- cloud storage integration
- Branch 3 AI/RAG deployment hooks
- Stage 06 high-performance C++ validation layer
