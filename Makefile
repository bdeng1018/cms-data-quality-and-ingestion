# ==============================================================================
# CMS Data Quality & Ingestion Pipeline — Makefile
# ==============================================================================

PYTHON := python

# ==============================================================================
# Help — Self‑Documenting Makefile
# ==============================================================================

.PHONY: help

help:
	@echo ""
	@echo "CMS Data Quality & Ingestion Pipeline — Commands"
	@echo "------------------------------------------------"
	@echo "make stage01            Run Stage 01 schema diagnostics"
	@echo "make stage02            Full Stage 02 (fetch → ingest → diag → lint → test)"
	@echo "make stage03            Run Stage 03 quality diagnostics"
	@echo "make fetch-pos          Download POS Q2 2026"
	@echo "make ingest-pos         Ingest POS parquet"
	@echo "make ingest-qies FILE=  Ingest QIES file"
	@echo "make diag-pos           Run POS ingestion diagnostics"
	@echo "make diag-qies FILE=    Run QIES ingestion diagnostics"
	@echo "make diag-quality       Run Stage 03 quality checks"
	@echo "make test               Run pytest suite"
	@echo "make lint               Run ruff + black checks"
	@echo "make clean-cache        Remove Python caches"
	@echo "make reset              Full cleanup of Stage 02 artifacts + logs"
	@echo "make env                Create conda environment from environment.yml"
	@echo ""

# ==============================================================================
# Stage 01 — Schema Diagnostics
# ==============================================================================

.PHONY: stage01 schema-diagnostics

stage01: schema-diagnostics lint
	@echo "Stage 01 complete."

schema-diagnostics:
	PYTHONPATH="$(PWD)/src:$(PWD)" $(PYTHON) scripts/diagnostics/stage01/check_schema.py

# ==============================================================================
# Stage 02 — Raw Ingestion (POS/QIES)
# ==============================================================================

.PHONY: stage02 fetch-pos ingest-pos ingest-qies diag-pos diag-qies

stage02: fetch-pos ingest-pos diag-pos lint test
	@echo "Stage 02 complete."

fetch-pos:
	$(PYTHON) src/stage02_raw_ingestion/fetch_pos_api.py \
		--out-parquet data/stage02_raw/pos_q2_2026.parquet \
		--out-csv data/stage02_raw/pos_q2_2026.csv

ingest-pos:
	PYTHONPATH="$(PWD)/src:$(PWD)" $(PYTHON) -m stage02_raw_ingestion.run_ingestion \
		pos data/stage02_raw/pos_q2_2026.parquet

ingest-qies:
	PYTHONPATH="$(PWD)/src:$(PWD)" $(PYTHON) -m stage02_raw_ingestion.run_ingestion \
		qies $(FILE)

diag-pos:
	PYTHONPATH="$(PWD)/src:$(PWD)" $(PYTHON) scripts/diagnostics/stage02/check_ingestion.py \
		pos data/stage02_raw/pos_q2_2026.parquet

diag-qies:
	PYTHONPATH="$(PWD)/src:$(PWD)" $(PYTHON) scripts/diagnostics/stage02/check_ingestion.py \
		qies $(FILE)

# ==============================================================================
# Stage 03 — Data Quality Profiling
# ==============================================================================

.PHONY: stage03 diag-quality

stage03: diag-quality lint test
	@echo "Stage 03 complete."

diag-quality:
	PYTHONPATH="$(PWD)/src:$(PWD)" $(PYTHON) scripts/diagnostics/stage03/check_quality.py \
		--file data/stage02_raw/pos_q2_2026.csv \
		--type pos

# ==============================================================================
# Testing
# ==============================================================================

.PHONY: test

test:
	PYTHONPATH="$(PWD)/src:$(PWD)" pytest tests

# ==============================================================================
# Linting
# ==============================================================================

.PHONY: lint

lint:
	ruff check .
	black --check .

# ==============================================================================
# Cache Cleanup
# ==============================================================================

.PHONY: clean-cache

clean-cache:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf .cache/
	rm -rf build/
	rm -rf dist/
	@echo "Cache cleaned."

# ==============================================================================
# Reset — Full Artifact Cleanup
# ==============================================================================

.PHONY: reset

reset: clean-cache
	rm -f data/stage02_raw/pos*
	rm -f data/stage02_raw/qies*
	rm -f logs/ingestion.log
	rm -f logs/quality.log
	@echo "Stage 02 + Stage 03 artifacts removed."

# ==============================================================================
# Environment Setup — Using environment.yml
# ==============================================================================

.PHONY: env

env:
	@echo "Creating conda environment from environment.yml..."
	conda env create -f environment.yml || echo "Environment already exists."
	@echo "To activate: conda activate pos_qies_pipeline"