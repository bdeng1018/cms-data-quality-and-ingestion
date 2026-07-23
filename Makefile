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
	@echo "STAGE RUNNERS:"
	@echo "  make stage01              Regenerate schema + run Stage 01 diagnostics"
	@echo "  make stage02              Run Stage 02 (fetch → ingest → clean → diagnostics)"
	@echo "  make stage03              Run Stage 03 (quality engine → diagnostics)"
	@echo "  make stage04              Run Stage 04 (reporting → diagnostics)"
	@echo "  make stage05              Run Stage 05 (pipeline runner → diagnostics)"
	@echo "  make run                  Run full pipeline (Stages 01–05)"
	@echo "  make smoke                Run lightweight smoke test (Stages 02–04)"
	@echo ""
	@echo "DIAGNOSTICS (ALL TARGETS):"
	@echo "  make diagnostics          Run ALL diagnostics (Stages 01–05)"
	@echo "  make schema-diagnostics   Stage 01 schema diagnostics"
	@echo "  make diag-pos             Stage 02 POS ingestion diagnostics"
	@echo "  make diag-qies FILE=...   Stage 02 QIES ingestion diagnostics"
	@echo "  make diag-cleaned         Stage 02 cleaned-data diagnostics"
	@echo "  make diag-quality         Stage 03 quality diagnostics"
	@echo "  make diag-intermediate    Stage 03 intermediate artifact diagnostics"
	@echo "  make diag-stage04         Stage 04 reporting diagnostics"
	@echo "  make diag-pipeline        Stage 05 pipeline runner diagnostics"
	@echo ""
	@echo "STAGE 02 INGESTION UTILITIES:"
	@echo "  make fetch-pos            Download POS Q2 2026"
	@echo "  make ingest-pos           Ingest POS parquet"
	@echo "  make ingest-qies FILE=... Ingest QIES file"
	@echo "  make clean-pos            Clean POS data"
	@echo ""
	@echo "TESTING & LINTING:"
	@echo "  make test                 Run pytest suite"
	@echo "  make lint                 Run ruff + black checks"
	@echo ""
	@echo "MAINTENANCE:"
	@echo "  make clean-cache          Remove Python caches"
	@echo "  make reset                Remove pipeline artifacts (keeps cleaned data)"
	@echo "  make env                  Create conda environment from environment.yml"
	@echo ""

# ==============================================================================
# Stage 01 — Schema Definition + Diagnostics
# ==============================================================================

.PHONY: stage01 regen-schema schema-diagnostics

stage01: regen-schema schema-diagnostics
	@echo "Stage 01 complete."

regen-schema:
	@echo "Regenerating schema.json from cleaned_data.csv..."
	PYTHONPATH="$(PWD)/src:$(PWD)" \
		$(PYTHON) scripts/diagnostics/stage01/generate_schema.py \
		--cleaned data/stage02_cleaned/cleaned_data.csv \
		--out data/stage01_schema/schema.json
	@echo "Schema regenerated."

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
	PYTHONPATH="$(PWD)/src:$(PWD)" $(PYTHON) -m stage02_raw_ingestion.run_cleaning

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
	PYTHONPATH="$(PWD)/src:$(PWD)" $(PYTHON) -m stage03_data_quality.run_quality

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

stage04: run-stage04 diag-stage04
	@echo "Stage 04 complete."

run-stage04:
	PYTHONPATH="$(PWD)/src:$(PWD)" \
		$(PYTHON) -m stage04_reporting.run_reporting

diag-stage04:
	PYTHONPATH="$(PWD)/src:$(PWD)" \
		$(PYTHON) scripts/diagnostics/stage04/check_reports.py

# ==============================================================================
# Stage 05 — Pipeline Runner (Orchestrator)
# ==============================================================================

.PHONY: stage05 run-stage05 diag-pipeline

stage05: run-stage05 diag-pipeline
	@echo "Stage 05 complete."

run-stage05:
	PYTHONPATH="$(PWD)/src:$(PWD)" \
		$(PYTHON) -m stage05_pipeline_runner.run_pipeline \
		--config configs/pipeline.yml \
		--output data/stage05_reports/pipeline_summary.json

diag-pipeline:
	PYTHONPATH="$(PWD)/src:$(PWD)" \
		$(PYTHON) scripts/diagnostics/stage05/check_pipeline.py

# ==============================================================================
# Full Pipeline — Stages 01–05
# ==============================================================================

.PHONY: run

run: stage01 stage02 stage03 stage04 stage05
	@echo "Full pipeline (Stages 01–05) complete."

# ==============================================================================
# Smoke Testing — Stages 02-04
# ==============================================================================

.PHONY: smoke

smoke: stage02 diag-cleaned stage03 diag-quality stage04
	@echo "Smoke test (Stages 02–04) complete."

# ==============================================================================
# Aggregate Diagnostics — All Stages
# ==============================================================================

.PHONY: diagnostics

# Left diag-qies out, but can include (between diag-pos and diag-cleaned)
diagnostics: schema-diagnostics diag-pos diag-cleaned diag-quality diag-intermediate diag-stage04 diag-pipeline
	@echo "All diagnostics (Stages 01–05) complete."

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
# Reset — Full Artifact Cleanup (SAFE: keeps Stage 02 cleaned data)
# ==============================================================================

.PHONY: reset

reset: clean-cache
	@read -p "This will delete ALL pipeline artifacts except cleaned data. Continue? (y/n) " ans; \
	if [ "$$ans" = "y" ]; then \
		rm -f data/stage02_raw/*; \
		rm -f data/stage03_intermediate/*; \
		rm -f data/stage04_processed/*; \
		rm -f data/stage05_reports/*; \
		rm -f logs/*.log; \
		echo "Pipeline artifacts (Stages 02–05) removed. Cleaned data preserved."; \
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