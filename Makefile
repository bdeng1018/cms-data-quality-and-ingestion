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
	@echo "make stage02            Full Stage 02 (fetch → ingest → clean → diag → lint → test)"
	@echo "make stage03            Full Stage 03 (run → diag → lint → test)"
	@echo "make stage04            Full Stage 04 (run → diag → lint → test)"
	@echo "make fetch-pos          Download POS Q2 2026"
	@echo "make ingest-pos         Ingest POS parquet"
	@echo "make ingest-qies FILE=  Ingest QIES file"
	@echo "make diag-pos           Run POS ingestion diagnostics"
	@echo "make diag-qies FILE=    Run QIES ingestion diagnostics"
	@echo "make diag-cleaned       Run Stage 02 cleaned-data diagnostics"
	@echo "make diag-quality       Run Stage 03 quality checks"
	@echo "make diag-intermediate  Validate Stage 03 intermediate artifacts"
	@echo "make diag-stage04       Validate Stage 04 processed artifacts"
	@echo "make test               Run pytest suite"
	@echo "make lint               Run ruff + black checks"
	@echo "make clean-cache        Remove Python caches"
	@echo "make reset              Full cleanup of Stage 02 artifacts + logs"
	@echo "make env                Create conda environment from environment.yml"
	@echo ""

# ==============================================================================
# Stage 01 — Schema Definition + Diagnostics
# ==============================================================================

.PHONY: stage01 schema regen-schema schema-diagnostics

# Full Stage 01 pipeline:
#   1. regenerate schema.json (automated)
#   2. run diagnostics
#   3. run lint
#   4. run tests
stage01: regen-schema schema-diagnostics
	@echo "Stage 01 complete."

# ------------------------------------------------------------------------------
# Automated Schema Regeneration (Branch 1)
# ------------------------------------------------------------------------------
# This regenerates schema.json from the canonical Stage 02 cleaned-data column list.
# It ensures schema.json always matches the pipeline.
regen-schema:
	@echo "Regenerating schema.json from cleaned_data.csv..."
	PYTHONPATH="$(PWD)/src:$(PWD)" \
		$(PYTHON) scripts/diagnostics/stage01/generate_schema.py \
		--cleaned data/stage02_cleaned/cleaned_data.csv \
		--out data/stage01_schema/schema.json
	@echo "Schema regenerated."

# ------------------------------------------------------------------------------
# Schema Diagnostics
# ------------------------------------------------------------------------------
schema-diagnostics:
	PYTHONPATH="$(PWD)/src:$(PWD)" \
		$(PYTHON) scripts/diagnostics/stage01/check_schema.py

# ==============================================================================
# Stage 02 — Raw Ingestion + Cleaning (POS/QIES)
# ==============================================================================

.PHONY: stage02 fetch-pos ingest-pos ingest-qies clean-pos diag-pos diag-qies diag-cleaned

stage02: fetch-pos ingest-pos clean-pos diag-cleaned
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

clean-pos:
	PYTHONPATH="$(PWD)/src:$(PWD)" $(PYTHON) -m src.stage02_raw_ingestion.run_cleaning

diag-pos:
	PYTHONPATH="$(PWD)/src:$(PWD)" $(PYTHON) scripts/diagnostics/stage02/check_ingestion.py \
		pos data/stage02_raw/pos_q2_2026.parquet

diag-qies:
	PYTHONPATH="$(PWD)/src:$(PWD)" $(PYTHON) scripts/diagnostics/stage02/check_ingestion.py \
		qies $(FILE)

diag-cleaned:
	PYTHONPATH="$(PWD)/src:$(PWD)" $(PYTHON) scripts/diagnostics/stage02/check_ingestion.py \
		cleaned data/stage02_cleaned/cleaned_data.csv

# ==============================================================================
# Stage 03 — Data Quality Profiling
# ==============================================================================

.PHONY: stage03 run-stage03 diag-quality diag-intermediate

stage03: run-stage03 diag-quality diag-intermediate
	@echo "Stage 03 complete."

run-stage03:
	PYTHONPATH="$(PWD)/src:$(PWD)" $(PYTHON) -m src.stage03_data_quality.run_quality

diag-quality:
	PYTHONPATH="$(PWD)/src:$(PWD)" $(PYTHON) scripts/diagnostics/stage03/check_quality.py \
		--file data/stage02_cleaned/cleaned_data.csv \
		--type pos

diag-intermediate:
	PYTHONPATH="$(PWD)/src:$(PWD)" $(PYTHON) scripts/diagnostics/stage03/check_intermediate_artifacts.py

# ==============================================================================
# Stage 04 — Reporting
# ==============================================================================

.PHONY: stage04 run-stage04 diag-stage04

# Full Stage 04 pipeline:
#   1. run reporting engine + formatter + writer
#   2. run diagnostics
#   3. run lint
#   4. run tests
stage04: run-stage04 diag-stage04
	@echo "Stage 04 complete."

run-stage04:
	PYTHONPATH="$(PWD)/src:$(PWD)" \
		$(PYTHON) -m src.stage04_reporting.run_reporting

diag-stage04:
	PYTHONPATH="$(PWD)/src:$(PWD)" \
		$(PYTHON) scripts/diagnostics/stage04/check_reports.py

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
	@read -p "This will delete ALL pipeline data. Continue? (y/n) " ans; \
	if [ "$$ans" = "y" ]; then \
		rm -f data/stage02_raw/*; \
		rm -f data/stage03_intermediate/*; \
		rm -f data/stage04_processed/*; \
		rm -f logs/*.log; \
		echo "Stage 02 + Stage 03 + Stage 04 artifacts and logs removed."; \
	else \
		echo "Reset aborted."; \
	fi

# ==============================================================================
# Environment Setup — Using environment.yml
# ==============================================================================

.PHONY: env

env:
	@echo "Creating conda environment from environment.yml..."
	conda env create -f environment.yml || echo "Environment already exists."
	@echo "To activate: conda activate pos_qies_pipeline"