# ==============================================================================
# CMS Data Quality & Ingestion Pipeline — Deterministic Deployment Image
# ==============================================================================
# Intent:
#   Provide a reproducible Docker image for executing the CMS ingestion pipeline
#   (Stages 01–05). The image ensures stable behavior, pinned Python version,
#   deterministic C++ mechanization, and a consistent filesystem layout for
#   artifact + manifest generation.
#
# Determinism Guarantees:
#   - Identical outputs given identical inputs.
#   - Pinned Python version (3.11).
#   - Deterministic C++ toolchain for mechanization.
#   - Stable directory structure under /app for artifacts, logs, and manifests.
# ==============================================================================

# ==============================================================================
# Base Image (Ubuntu-based, ARM64-stable)
# ==============================================================================
FROM python:3.11 AS base

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
# System Dependencies (Deterministic C++ Mechanization)
# ==============================================================================
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    ninja-build && \
    rm -rf /var/lib/apt/lists/*

# ==============================================================================
# Dependency Contracts
# ==============================================================================
COPY environment.yml ./
COPY deployment/requirements.txt ./deployment/requirements.txt

# ==============================================================================
# Deterministic Dependency Installation (pip)
# ==============================================================================
RUN pip install --upgrade pip && \
    pip install -r deployment/requirements.txt

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
COPY Makefile /app/Makefile
COPY deployment/Makefile.deploy /app/deployment/Makefile.deploy

# ==============================================================================
# Artifact + Log Directories
# ==============================================================================
RUN mkdir -p /app/data /app/logs

# ==============================================================================
# CLI Entrypoint
# ==============================================================================
ENTRYPOINT ["python", "-m", "src.stage05_pipeline_runner.run_pipeline"]
