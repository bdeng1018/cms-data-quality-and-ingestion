# ==============================================================================
# CMS Data Quality & Ingestion Pipeline (Deterministic Deployment Image)
# ==============================================================================
# Intent:
#   Provide a reproducible, contract-driven Docker image for executing the CMS
#   ingestion pipeline (Stages 01–05). This image ensures deterministic behavior,
#   pinned dependencies, isolated artifacts, and stable provenance fields recorded
#   in manifest.json.
#
# Determinism Guarantees:
#   - Identical outputs given identical inputs.
#   - Pinned Python + dependency versions via uv.
#   - No dynamic dependency resolution.
#   - Stable filesystem layout for artifact + manifest generation.
#
# Side Effects:
#   - Writes artifacts to /app/data.
#   - Writes logs to /app/logs.
#   - Produces manifest + artifact registry in Stage 05.
#
# Future Extensions:
#   - Replace entrypoint with `cms run` after CLI implementation.
#   - Add healthcheck for long-running ingestion jobs.
#   - Integrate with K8s/Helm/Terraform deployment layers.
# ==============================================================================


# ==============================================================================
# Base Image
# ==============================================================================
# Intent:
#   Use a modern, slim, deterministic Python base image to minimize nondeterminism
#   and reduce attack surface.
#
# Determinism:
#   - Python version pinned (3.11).
#   - Slim variant reduces OS-level variability.
# ==============================================================================
FROM python:3.11-slim AS base


# ==============================================================================
# Environment Setup
# ==============================================================================
# Intent:
#   Configure Python runtime for deterministic behavior and clean logging.
#
# Determinism:
#   - Prevents .pyc creation.
#   - Ensures unbuffered output for stable logs.
# ==============================================================================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# ==============================================================================
# System Dependencies
# ==============================================================================
# Intent:
#   Install minimal system dependencies required for ingestion, diagnostics, and
#   reproducible builds.
#
# Determinism:
#   - No optional packages.
#   - No dynamic apt sources.
# ==============================================================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*


# ==============================================================================
# Working Directory
# ==============================================================================
# Intent:
#   Establish deterministic filesystem layout for pipeline execution.
#
# Side Effects:
#   - All artifacts/logs/manifests written under /app.
# ==============================================================================
WORKDIR /app


# ==============================================================================
# Dependency Files
# ==============================================================================
# Intent:
#   Copy dependency definitions into the image. These will later replace
#   environment.yml with pyproject.toml + uv.lock.
#
# Determinism:
#   - uv.lock ensures frozen dependency resolution.
# ==============================================================================
COPY pyproject.toml uv.lock ./


# ==============================================================================
# Deterministic Dependency Installation
# ==============================================================================
# Intent:
#   Install Python dependencies deterministically using uv.
#
# Determinism:
#   - uv sync --frozen prevents dependency drift.
#   - pip upgraded deterministically.
# ==============================================================================
RUN pip install --upgrade pip \
    && pip install uv \
    && uv sync --frozen


# ==============================================================================
# Pipeline Source Code
# ==============================================================================
# Intent:
#   Copy all pipeline code, configs, diagnostics, and deployment contracts into
#   the image. These directories are mounted read-only in docker-compose.yml.
#
# Determinism:
#   - Stable directory structure ensures reproducible artifact paths.
# ==============================================================================
COPY src/ ./src/
COPY utils/ ./utils/
COPY configs/ ./configs/
COPY scripts/ ./scripts/
COPY deployment/ ./deployment/


# ==============================================================================
# Makefiles + CLI Entrypoints
# ==============================================================================
# Intent:
#   Provide deterministic build + execution tooling inside the container.
#
# Future Extension:
#   Replace entrypoint with `cms run` after CLI implementation.
# ==============================================================================
COPY Makefile .
COPY deployment/Makefile.deploy .


# ==============================================================================
# Data + Log Directories
# ==============================================================================
# Intent:
#   Create directories for artifacts and logs. These are writable mounts in
#   docker-compose.yml.
#
# Side Effects:
#   - Artifacts written to /app/data.
#   - Logs written to /app/logs.
# ==============================================================================
RUN mkdir -p data logs


# ==============================================================================
# CLI Entrypoint
# ==============================================================================
# Intent:
#   Provide deterministic pipeline execution via Stage 05 runner.
#
# Future Extension:
#   Replace with `cms run` after CLI implementation.
#   See: Create CMS CLI
# ==============================================================================
ENTRYPOINT ["python", "-m", "src.stage05_pipeline_runner.run_pipeline"]