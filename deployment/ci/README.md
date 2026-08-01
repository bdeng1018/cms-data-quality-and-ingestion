# CMS Data Quality & Ingestion Pipeline — CI/CD Workflow Documentation

## Documentation Contract

This README defines the deterministic CI/CD workflow for the CMS Data Quality &
Ingestion Pipeline. It explains how GitHub Actions enforces reproducible builds,
tests, manifest validation, artifact registry validation, and Docker image
construction.

### Determinism Guarantees

- pinned Python version  
- pinned dependency installation via uv  
- stable job names and workflow ordering  
- reproducible Docker builds  
- deterministic validation steps  

### Side Effects

- executes tests  
- validates manifests + artifact registry  
- builds Docker image  
- optionally publishes image to registry  

---

## Overview

The CI/CD workflow (`github-actions.yml`) provides a deterministic execution
environment that mirrors local development, docker-compose, and Kubernetes
deployment behavior.

The workflow ensures:

- reproducible dependency installation  
- deterministic test execution  
- stable diagnostics + validation  
- reproducible Docker image builds  
- optional publishing to container registry  

This workflow is designed to be:

- contract-driven  
- reproducible  
- provenance-aware  
- environment-agnostic  

---

## Workflow Structure

The CI/CD pipeline contains two jobs:

### 1. **build-test-validate**

Runs on every push and pull request to `main`.

Includes:

- repository checkout  
- Python setup (pinned version)  
- deterministic dependency installation (`uv sync --frozen`)  
- test execution  
- manifest validation  
- artifact registry validation  
- Docker image build  

### 2. **publish**

Runs only on `main` after successful validation.

Includes:

- registry login  
- Docker image build  
- optional push to registry  

---

## Deterministic Dependency Installation

Dependencies are installed using:

```bash
pip install uv
uv sync --frozen
```

This ensures:

- no dynamic dependency resolution  
- pinned versions from `uv.lock`  
- reproducible builds across environments  

---

## Validation Steps

The CI/CD workflow validates:

### Manifest

```bash
python scripts/diagnostics/stage05/check_pipeline.py
```

Ensures:

- required fields exist  
- keys are sorted  
- provenance fields match environment  

### Artifact Registry

```bash
python scripts/diagnostics/stage04/check_reports.py
```

Ensures:

- all artifacts are present  
- hashes match actual files  
- schema version is correct  

These validations enforce pipeline contract compliance.

---

## Docker Image Build (Deterministic)

The workflow builds the deterministic deployment image:

```bash
docker build -f deployment/Dockerfile -t cms_ingestion:ci .
```

This mirrors:

- local docker-compose builds  
- K8s deployment image  
- Helm chart image  

---

## Optional Publishing

If desired, the workflow can push the image to a registry:

```bash
docker push <registry>/cms_ingestion:latest
```

This step is disabled by default and requires:

- `DOCKER_USERNAME`  
- `DOCKER_PASSWORD`  

stored in GitHub Secrets.

---

## Reproducibility Contract

The CI/CD workflow **must**:

- use pinned Python version  
- use pinned dependency versions  
- run validation steps in fixed order  
- build Docker image deterministically  
- avoid nondeterministic environment behavior  
- preserve artifact isolation  

These rules ensure CI/CD behaves identically across:

- local development  
- docker-compose  
- Kubernetes  
- Helm  
- cloud deployment  

---

## Future Extensions

This CI/CD workflow is designed to evolve into a full ingestion platform:

- multi-stage Docker builds  
- distributed ingestion tests  
- cloud storage integration tests  
- K8s deployment automation  
- Helm chart publishing  
- Terraform provisioning automation  
- RAG/AI indexing pipeline integration  
