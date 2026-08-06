# ==============================================================================
# CMS Data Quality & Ingestion Pipeline — Makefile
# ==============================================================================

VERSION ?= dev
PYTHON := python
PYTHONPATH := "$(PWD):$(PWD)/src:$(PWD)/scripts"

# ==============================================================================
# Help — Self‑Documenting Makefile
# ==============================================================================

.PHONY: help

help:
	@echo ""
	@echo "CMS Data Quality & Ingestion Pipeline — Commands"
	@echo "------------------------------------------------"
	@grep -E '^[a-zA-Z0-9_-]+:.*##' Makefile \
		| sed -E 's/^(.*):.*##(.*)/\1:\2/' \
		| sed -E 's/^([^:]+):/\1:  /'
	@echo ""

# ==============================================================================
# Stage 01 — Schema Definition + Diagnostics
# ==============================================================================

.PHONY: stage01 regen-schema schema-diagnostics

stage01: regen-schema schema-diagnostics ## Regenerate schema + run Stage 01 diagnostics
	@echo "Stage 01 complete."

regen-schema: ## Regenerate schema.json from cleaned_data.csv
	@mkdir -p data/stage01_schema
	@echo "Regenerating schema.json from cleaned_data.csv..."
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) scripts/diagnostics/stage01/generate_schema.py \
		--cleaned data/stage02_cleaned/cleaned_data.csv \
		--out data/stage01_schema/schema.json
	@echo "Schema regenerated."

schema-diagnostics: ## Run Stage 01 schema diagnostics
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) scripts/diagnostics/stage01/check_schema.py

# ==============================================================================
# Stage 02 — Raw Ingestion + Cleaning (POS/QIES)
# ==============================================================================

.PHONY: stage02 fetch-pos ingest-pos ingest-qies clean-pos diag-pos diag-qies diag-cleaned

stage02: fetch-pos ingest-pos clean-pos diag-cleaned ## Stage 02 — ingestion + cleaning
	@echo "Stage 02 complete."

fetch-pos: ## Download POS Q2 2026
	@mkdir -p data/stage02_raw
	$(PYTHON) src/stage02_raw_ingestion/fetch_pos_api.py \
		--out-parquet data/stage02_raw/pos_q2_2026.parquet \
		--out-csv data/stage02_raw/pos_q2_2026.csv

ingest-pos: ## Ingest POS parquet
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m stage02_raw_ingestion.run_ingestion \
		pos data/stage02_raw/pos_q2_2026.parquet

ingest-qies: ## Ingest QIES file (FILE=...)
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m stage02_raw_ingestion.run_ingestion \
		qies $(FILE)

clean-pos: ## Clean POS data
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m stage02_raw_ingestion.run_cleaning

diag-pos: ## Diagnostics for POS ingestion
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/diagnostics/stage02/check_ingestion.py \
		pos data/stage02_raw/pos_q2_2026.parquet

diag-qies: ## Diagnostics for QIES ingestion (FILE=...)
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/diagnostics/stage02/check_ingestion.py \
		qies $(FILE)

diag-cleaned: ## Diagnostics for cleaned Stage 02 data
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/diagnostics/stage02/check_ingestion.py \
		cleaned data/stage02_cleaned/cleaned_data.csv

# ==============================================================================
# Stage 03 — Data Quality Profiling
# ==============================================================================

.PHONY: stage03 run-stage03 diag-quality diag-intermediate

stage03: run-stage03 diag-quality diag-intermediate ## Stage 03 — quality profiling
	@echo "Stage 03 complete."

run-stage03: ## Run Stage 03 quality engine
	@mkdir -p data/stage03_intermediate
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m stage03_data_quality.run_quality

diag-quality: ## Stage 03 quality diagnostics
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/diagnostics/stage03/check_quality.py \
		--file data/stage02_cleaned/cleaned_data.csv \
		--type pos

diag-intermediate: ## Diagnostics for Stage 03 intermediate artifacts
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/diagnostics/stage03/check_intermediate_artifacts.py

# ==============================================================================
# Stage 04 — Reporting
# ==============================================================================

.PHONY: stage04 run-stage04 diag-stage04

stage04: run-stage04 diag-stage04 ## Stage 04 — reporting
	@echo "Stage 04 complete."

run-stage04: ## Run Stage 04 reporting
	@mkdir -p data/stage04_processed
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) -m stage04_reporting.run_reporting

diag-stage04: ## Stage 04 reporting diagnostics
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) scripts/diagnostics/stage04/check_reports.py

# ==============================================================================
# Stage 05 — Pipeline Runner (Orchestrator)
# ==============================================================================

.PHONY: stage05 run-stage05 diag-pipeline

stage05: run-stage05 diag-pipeline ## Stage 05 — pipeline runner
	@echo "Stage 05 complete."

run-stage05: ## Run Stage 05 pipeline orchestrator
	@mkdir -p data/stage05_reports
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) -m stage05_pipeline_runner.run_pipeline \
		--config configs/pipeline.yml \
		--output data/stage05_reports/pipeline_summary.json

diag-pipeline: ## Stage 05 pipeline diagnostics
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) scripts/diagnostics/stage05/check_pipeline.py

# ==============================================================================
# Full Pipeline — Stages 01–05
# ==============================================================================

.PHONY: run
run: stage02 stage01 stage03 stage04 stage05 ## Run full pipeline (Stages 01–05)
	@echo "Full pipeline (Stages 01–05) complete."

# ==============================================================================
# Smoke Testing — Stages 02-04
# ==============================================================================

.PHONY: smoke
smoke: stage02 diag-cleaned stage03 diag-quality stage04 ## Smoke test (Stages 02–04)
	@echo "Smoke test (Stages 02–04) complete."

# ==============================================================================
# Aggregate Diagnostics — All Stages
# ==============================================================================

.PHONY: diagnostics
diagnostics: diag-pos diag-cleaned schema-diagnostics diag-quality diag-intermediate diag-stage04 diag-pipelieI ## Run all diagnostics
	@echo "All diagnostics (Stages 01–05) complete."

# ==============================================================================
# Testing
# ==============================================================================

.PHONY: test
test: ## Run pytest suite
	PYTHONPATH=$(PYTHONPATH) pytest tests

# ==============================================================================
# Linting
# ==============================================================================

.PHONY: lint
lint: ## Run ruff + black checks
	ruff check .
	black --check .

# ==============================================================================
# Cache Cleanup
# ==============================================================================

.PHONY: clean-cache
clean-cache: ## Remove Python caches
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
reset: clean-cache ## Remove pipeline artifacts (keeps cleaned data)
	@read -p "This will delete ALL pipeline artifacts except cleaned data. Continue? (y/n) " ans; \
	if [ "$$ans" = "y" ]; then \
		rm -f data/stage02_raw/*; \
		rm -f data/stage03_intermediate/*; \
		rm -f data/stage04_processed/*; \
		rm -f data/stage05_reports/*; \
		rm -f logs/*.log; \
		@echo "Pipeline artifacts (Stages 02–05) removed. Cleaned data preserved."; \
	else \
		@echo "Reset aborted."; \
	fi

# ==============================================================================
# Environment Setup — Using environment.yml
# ==============================================================================

.PHONY: env
env: ## Create conda environment
	@echo "Creating conda environment from environment.yml..."
	conda env create -f environment.yml || echo "Environment already exists."
	@echo "To activate: conda activate pos_qies_pipeline"

# ==============================================================================
# Deployment Layer Integration
# ==============================================================================

.PHONY: deploy
deploy: ## Run deployment orchestrator (delegates to deployment/Makefile.deploy)
	@echo "Running deployment orchestrator..."
	$(MAKE) -f deployment/Makefile.deploy deploy
	@echo "Deployment complete."

# ==============================================================================
# Provenance Validation
# ==============================================================================

.PHONY: provenance
provenance: ## Validate provenance for a version (VERSION=...)
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) deployment/scripts/validate_provenance.py $(VERSION)

# ==============================================================================
# SBOM Validation
# ==============================================================================

.PHONY: sbom
sbom: ## Validate SBOM for a version (VERSION=...)
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) deployment/scripts/validate_sbom.py $(VERSION)

# ==============================================================================
# Freeze
# ==============================================================================

.PHONY: freeze
freeze: ## Freeze pipeline version (VERSION=...)
	$(PYTHON) deployment/scripts/bump_version.py $(VERSION)
	$(PYTHON) deployment/scripts/freeze_runner.py $(VERSION)

# ==============================================================================
# Drift Detection — Terraform + Helm
# ==============================================================================

.PHONY: drift
drift: ## Detect deployment drift (Terraform + Helm diff)
	@echo "Checking Terraform drift..."
	cd deployment/terraform && terraform plan -detailed-exitcode || true
	@echo "Checking Helm diff..."
	helm diff upgrade cms-pipeline deployment/helm --values deployment/helm/values.yml || true
	@echo "Drift detection complete."

# ==============================================================================
# Audit Log Generation
# ==============================================================================

.PHONY: audit
audit: ## Generate audit logs for deployment + pipeline
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) deployment/scripts/generate_audit_logs.py \
		--manifest deployment/provenance/provenance-$(VERSION).json \
		--sbom deployment/sbom/sbom-$(VERSION).json \
		--out logs/audit.log
	@echo "Audit log generated."
