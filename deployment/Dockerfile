# ==============================================================================
# CMS Data Quality & Ingestion Pipeline — Deterministic Deployment Image
# ==============================================================================
# Intent:
#   Provide a reproducible Docker image for executing the CMS ingestion pipeline
#   (Stages 01–05). The image ensures stable behavior, pinned Python version,
#   and a consistent filesystem layout for artifact + manifest generation.
#
# Determinism Guarantees:
#   - Identical outputs given identical inputs.
#   - Pinned Python version (3.11).
#   - Stable directory structure under /app for artifacts, logs, and manifests.
#
# Side Effects:
#   - Artifacts written to /app/data.
#   - Logs written to /app/logs.
#   - Stage 05 produces manifest + provenance registry.
#
# Future Extensions:
#   - Replace entrypoint with `cms run` after CLI implementation.
#   - Add healthcheck for long-running ingestion jobs.
#   - Integrate with K8s/Helm/Terraform deployment layers.
# ==============================================================================

# ==============================================================================
# Base Image
# ==============================================================================
FROM python:3.11-slim AS base

# ==============================================================================
# OCI Source Label (GHCR Linking)
# ==============================================================================
LABEL org.opencontainers.image.source="https://github.com/bdeng1018/cms-data-quality-and-ingestion"

# ==============================================================================
# Environment Setup
# ==============================================================================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"

# ==============================================================================
# Working Directory
# ==============================================================================
WORKDIR /app

# ==============================================================================
# Dependency Contracts
# ==============================================================================
COPY environment.yml ./
COPY deployment/requirements.txt ./

# ==============================================================================
# Deterministic Dependency Installation (pip)
# ==============================================================================
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# ==============================================================================
# Pipeline Source Code
# ==============================================================================
COPY src/ /app/src/
COPY utils/ /app/utils/
COPY configs/ /app/configs/
COPY scripts/ /app/scripts/
COPY deployment/ /app/deployment/

# ==============================================================================
# Makefiles + CLI Entrypoints
# ==============================================================================
COPY Makefile .
COPY deployment/Makefile.deploy .

# ==============================================================================
# Artifact + Log Directories
# ==============================================================================
RUN mkdir -p data logs

# ==============================================================================
# CLI Entrypoint
# ==============================================================================
ENTRYPOINT ["python", "-m", "src.stage05_pipeline_runner.run_pipeline"]
