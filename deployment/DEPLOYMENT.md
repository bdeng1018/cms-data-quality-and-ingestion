# CMS Data Quality & Ingestion Pipeline — Deployment Specification

## 1. Overview

This document defines the deployment architecture, environment guarantees, execution pathways, and operational expectations for the CMS Data Quality & Ingestion Pipeline (Stages 01–05). Deployment is contract‑driven and designed for deterministic, reproducible, and isolated execution across local, Docker, and CI/CD environments.

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
- Makefile targets  
- Python entrypoints  

### 2.2 Environment Layer

- Docker image  
- pinned Python dependencies  
- reproducible runtime  

### 2.3 Orchestration Layer

- pipeline runner  
- manifest writer  
- artifact registry  
- provenance tracker  

### 2.4 Validation Layer

- diagnostics scripts  
- schema validation  
- quality checks  
- reporting checks  

Each layer is deterministic and contract‑driven.

---

## 3. Supported Execution Modes

### 3.1 Local Development

Local execution uses:

- `uv` or `pip-tools` for dependency management  
- CLI commands  
- Makefile targets  
- local logs + artifacts  

Local runs must produce identical manifests, artifacts, and diagnostics given identical inputs.

### 3.2 Dockerized Execution

Docker execution provides:

- reproducible environment  
- pinned Python + OS dependencies  
- isolated filesystem  
- deterministic logs  

Docker runs must produce bit‑for‑bit identical artifacts to local runs.

### 3.3 CI/CD Execution

CI/CD runs:

- linting  
- tests  
- Docker build  
- manifest validation  
- artifact registry validation  
- release artifact publishing  

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

### 4.2 Docker Image

The Docker image must:

- pin Python version  
- install dependencies deterministically  
- include CLI entrypoints  
- include diagnostics scripts  
- mount input/output directories  

### 4.3 CI/CD Pipeline

CI/CD must:

- run full test suite  
- lint code  
- build Docker image  
- validate manifest schema  
- validate artifact registry  
- publish release artifacts  

Release artifacts include:

- Docker image  
- manifest schema  
- artifact registry schema  
- deployment diagrams  

### 4.4 Manifests

Manifests must include:

- run metadata  
- timestamps  
- duration  
- config hash  
- environment hash  
- artifact index  
- diagnostics summary  

Manifest schema is defined in `MANIFEST_SPEC.md`.

### 4.5 Artifact Registry

The artifact registry must:

- list all produced artifacts  
- include paths + hashes  
- include schema versions  
- include diagnostics status  

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

Given identical inputs, two runs must produce:

- identical manifests  
- identical artifacts  
- identical diagnostics  

---

## 6. Operational Expectations

### 6.1 Logging

Logs must include:

- timestamps  
- stage boundaries  
- warnings  
- errors  
- duration metrics  

### 6.2 Diagnostics

Diagnostics must validate:

- schema  
- ingestion  
- intermediate artifacts  
- reporting artifacts  
- pipeline summary  

### 6.3 Error Handling

Errors must:

- be deterministic  
- include stage + file + line  
- include remediation hints  
- never produce partial artifacts  

---

## 7. Deployment Directory Structure

```text
deployment/
    DEPLOYMENT.md
    CONTRACTS.md
    MANIFEST_SPEC.md
    OPERATIONS.md
    Dockerfile
    compose.yml
    Makefile.deploy
    k8s/
    helm/
    terraform/
    env/
```

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
