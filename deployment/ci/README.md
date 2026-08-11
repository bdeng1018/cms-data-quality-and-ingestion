# CMS Data Quality & Ingestion Pipeline — CI/CD Workflow Documentation

## Documentation Contract

This README defines the deterministic CI/CD workflow for the CMS Data Quality &
Ingestion Pipeline. It explains how GitHub Actions enforces reproducible builds,
tests, mechanization validation, manifest validation, artifact registry
validation, and Docker image construction.

### Determinism Guarantees

- pinned Python version
- pinned dependency installation via uv
- deterministic C++ toolchain installation
- deterministic C++ mechanization builds
- stable job names and workflow ordering
- reproducible Docker builds
- deterministic validation steps

### Side Effects

- executes Python + C++ tests
- validates manifests + artifact registry
- validates mechanization outputs
- builds Docker image (with C++ mechanization)
- optionally publishes image to registry

---

## Overview

The CI/CD workflow (`github-actions.yml`) provides a deterministic execution
environment that mirrors local development, docker-compose, and Kubernetes
deployment behavior.

The workflow ensures:

- reproducible dependency installation
- deterministic Python + C++ test execution
- stable diagnostics + validation
- reproducible Docker image builds
- optional publishing to container registry

This workflow is designed to be:

- contract-driven
- reproducible
- provenance-aware
- environment-agnostic
- mechanization-aware (python-only vs python+cpp)

---

## Workflow Structure

The CI/CD pipeline contains two jobs:

### 1. **build-test-validate**

Runs on every push and pull request to `main`.

Includes:

- repository checkout
- Python setup (pinned version)
- deterministic dependency installation (`uv sync --frozen`)
- deterministic C++ toolchain installation
- C++ mechanization build (`make cpp-all`)
- Python test execution
- C++ mechanization test execution (`pytest -m cpp_all`)
- manifest validation
- artifact registry validation
- Docker image build (with mechanization)

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

## Deterministic C++ Toolchain Installation

The workflow installs a deterministic C++ toolchain:

```bash
sudo apt-get update
sudo apt-get install -y g++ make cmake ninja-build
```

This ensures:

- reproducible C++ builds
- deterministic mechanization behavior
- CI/CD parity with Dockerfile builds

---

## C++ Mechanization Build

The mechanization layer is built using:

```bash
make cpp-all
```

This compiles:

- C++ schema validator
- C++ row counter
- C++ ingestion utilities

All binaries must be deterministic across CI/CD and Docker.

---

## Test Execution

### Python Tests

```bash
make test
```

### C++ Mechanization Tests

```bash
pytest -m cpp_all
```

These tests validate:

- C++ schema validator correctness
- C++ row counter correctness
- deterministic mechanization behavior

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
- mechanization mode is correct
- C++ exit codes are recorded

### Artifact Registry

```bash
python scripts/diagnostics/stage04/check_reports.py
```

Ensures:

- all artifacts are present
- hashes match actual files
- schema version is correct
- mechanization outputs are included

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
- mechanization-enabled runtime environment

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
- install deterministic C++ toolchain
- build C++ mechanization deterministically
- run validation steps in fixed order
- build Docker image deterministically
- avoid nondeterministic environment behavior
- preserve artifact isolation
- produce identical mechanization outputs across runs

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
- mechanization performance benchmarking
