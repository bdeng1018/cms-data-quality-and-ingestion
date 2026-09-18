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

.PHONY: stage01 regen-schema schema-diagnostics diag-cpp-schema-validator diag-cpp-schema-wrapper

stage01: regen-schema schema-diagnostics diag-cpp-schema-validator diag-cpp-schema-wrapper ## Regenerate schema + run Stage 01 diagnostics
	@echo "Stage 01 complete."

regen-schema: ## Regenerate schema.json from cleaned_data.csv
	@mkdir -p data/stage01_schema
	@echo "Regenerating schema.json from cleaned_data.csv..."
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) scripts/diagnostics/stage01/generate_schema.py \
		--cleaned data/stage02_cleaned/cleaned_data.csv \
		--out data/stage01_schema/schema.json
	@echo "Schema regenerated."

schema-diagnostics: ## Run Stage 01 schema diagnostics (Python)
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) scripts/diagnostics/stage01/check_schema.py

diag-cpp-schema-validator: ## Run Stage 01 C++ schema validator diagnostics
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) scripts/diagnostics/stage01/check_cpp_schema_validator.py

diag-cpp-schema-wrapper: ## Run Stage 01 C++ schema wrapper diagnostics
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) scripts/diagnostics/stage01/check_cpp_schema_wrapper.py

# ==============================================================================
# Stage 02 — Raw Ingestion + Cleaning (POS/QIES)
# ==============================================================================

.PHONY: stage02 fetch-pos ingest-pos ingest-qies clean-pos \
		diag-pos diag-qies diag-cleaned \
		diag-cpp-row-counter diag-cpp-row-counter-wrapper diag-ingestion-metadata

stage02: fetch-pos ingest-pos clean-pos diag-pos diag-cleaned diag-cpp-row-counter diag-cpp-row-counter-wrapper diag-ingestion-metadata ## Stage 02 — ingestion + cleaning + diagnostics
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

diag-cpp-row-counter: ## Diagnostics for C++ row counter
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) scripts/diagnostics/stage02/check_cpp_row_counter.py

diag-cpp-row-counter-wrapper: ## Diagnostics for C++ row counter wrapper
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) scripts/diagnostics/stage02/check_cpp_row_counter_wrapper.py

diag-ingestion-metadata: ## Diagnostics for ingestion metadata
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) scripts/diagnostics/stage02/check_ingestion_metadata.py

# ==============================================================================
# Stage 03 — Data Quality Profiling
# ==============================================================================

.PHONY: stage03 run-stage03 \
        diag-quality diag-intermediate diag-quality-contract

stage03: run-stage03 diag-quality diag-intermediate diag-quality-contract ## Stage 03 — quality profiling + diagnostics
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

diag-quality-contract: ## Stage 03 quality contract diagnostics
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/diagnostics/stage03/check_quality_contract.py

# ==============================================================================
# Stage 04 — Reporting
# ==============================================================================

.PHONY: stage04 run-stage04 diag-stage04 diag-report-contract

stage04: run-stage04 diag-stage04 diag-report-contract ## Stage 04 — reporting + diagnostics
	@echo "Stage 04 complete."

run-stage04: ## Run Stage 04 reporting
	@mkdir -p data/stage04_processed
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) -m stage04_reporting.run_reporting

diag-stage04: ## Stage 04 reporting diagnostics
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) scripts/diagnostics/stage04/check_reports.py

diag-report-contract: ## Stage 04 report contract diagnostics
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) scripts/diagnostics/stage04/check_report_contract.py

# ==============================================================================
# Stage 05 — Pipeline Runner (Orchestrator)
# ==============================================================================

.PHONY: stage05 run-stage05 \
		diag-pipeline diag-pipeline-contract \
		diag-mechanization-logs diag-mechanization-provenance

stage05: run-stage05 diag-pipeline diag-pipeline-contract diag-mechanization-logs diag-mechanization-provenance ## Stage 05 — pipeline runner + diagnostics
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

diag-pipeline-contract: ## Stage 05 pipeline contract diagnostics
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) scripts/diagnostics/stage05/check_pipeline_contract.py

diag-mechanization-logs: ## Stage 05 mechanization log diagnostics
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) scripts/diagnostics/stage05/check_mechanization_logs.py

diag-mechanization-provenance: ## Stage 05 mechanization provenance diagnostics
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) scripts/diagnostics/stage05/check_mechanization_provenance.py

# ==============================================================================
# Utils Diagnostics — File I/O + Logging
# ==============================================================================

.PHONY: diag-file-io diag-logging-utils

diag-file-io: ## Diagnostics for file I/O determinism
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) scripts/diagnostics/utils/check_file_io.py

diag-logging-utils: ## Diagnostics for logging determinism
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) scripts/diagnostics/utils/check_logging_utils.py

# ==============================================================================
# Utils C++ Diagnostics — Mechanization Contract
# ==============================================================================

.PHONY: diag-utils-cpp

diag-utils-cpp: ## Diagnostics for C++ mechanization utilities contract
	PYTHONPATH=$(PYTHONPATH) \
		$(PYTHON) scripts/diagnostics/utils_cpp/check_utils_cpp_contract.py

# ==============================================================================
# Full Pipeline — Stages 01–05
# ==============================================================================

.PHONY: run
run: cpp-all stage02 stage01 stage03 stage04 stage05 ## Run full pipeline (Stages 01–05)
	@echo "Full pipeline (Stages 01–05) complete."

# ==============================================================================
# Smoke Testing — Stages 02–04
# ==============================================================================

.PHONY: smoke
smoke: ## Smoke test (Stages 02–04)
	## Stage 02
	$(MAKE) stage02
	$(MAKE) diag-pos
	$(MAKE) diag-cleaned
	$(MAKE) diag-cpp-row-counter
	$(MAKE) diag-cpp-row-counter-wrapper
	$(MAKE) diag-ingestion-metadata

	## Stage 03
	$(MAKE) stage03
	$(MAKE) diag-quality
	$(MAKE) diag-intermediate
	$(MAKE) diag-quality-contract

	## Stage 04
	$(MAKE) stage04
	$(MAKE) diag-stage04
	$(MAKE) diag-report-contract

	@echo "Smoke test (Stages 02–04) complete."

# ==============================================================================
# Aggregate Diagnostics — All Stages
# ==============================================================================

.PHONY: diagnostics
diagnostics: ## Run all diagnostics
	## Stage 01
	$(MAKE) schema-diagnostics
	$(MAKE) diag-cpp-schema-validator
	$(MAKE) diag-cpp-schema-wrapper

	## Stage 02
	$(MAKE) diag-pos
	$(MAKE) diag-cleaned
	$(MAKE) diag-cpp-row-counter
	$(MAKE) diag-cpp-row-counter-wrapper
	$(MAKE) diag-ingestion-metadata

	## Stage 03
	$(MAKE) diag-quality
	$(MAKE) diag-intermediate
	$(MAKE) diag-quality-contract

	## Stage 04
	$(MAKE) diag-stage04
	$(MAKE) diag-report-contract

	## Stage 05
	$(MAKE) diag-pipeline
	$(MAKE) diag-pipeline-contract
	$(MAKE) diag-mechanization-logs
	$(MAKE) diag-mechanization-provenance

	## Utils
	$(MAKE) diag-file-io
	$(MAKE) diag-logging-utils

	## Utils C++
	$(MAKE) diag-utils-cpp

	@echo "All diagnostics (Stages 01–05 + utils + utils_cpp) complete."

# ==============================================================================
# Testing
# ==============================================================================

.PHONY: test python-tests

test: ## Run pytest suite
	PYTHONPATH=$(PYTHONPATH) pytest tests

python-tests: cpp-all ## Build C++ binaries then run pytest
	PYTHONPATH=$(PYTHONPATH) pytest tests

# ==============================================================================
# Linting
# ==============================================================================

.PHONY: lint
lint: ## Run ruff + black checks
	ruff check .
	black --check .

# ==============================================================================
# Formatting
# ==============================================================================

.PHONY: format
format: ## Auto-format Python code
	black src/ scripts/ tests/

# ==============================================================================
# C++ Mechanization Utilities
# ==============================================================================

.PHONY: cpp-utils cpp-schema cpp-all

UTILS_CPP_DIR = src/utils_cpp
STAGE01_CPP_DIR = src/stage01_schema_definition

tests/utils_cpp: ## Create utils_cpp/ directory under tests/ (if applicable)
	mkdir -p tests/utils_cpp

cpp-utils: tests/utils_cpp ## Build deterministic C++ mechanization utilities for ingestion diagnostics
	@echo "[cpp-utils] Building C++ mechanization utilities..."

	# Build csv_row_counter for pytest
	g++ -O2 -std=c++17 $(UTILS_CPP_DIR)/csv_row_counter.cpp -o tests/utils_cpp/csv_row_counter

	# Build csv_row_counter for pipeline diagnostics
	g++ -O2 -std=c++17 $(UTILS_CPP_DIR)/csv_row_counter.cpp -o $(UTILS_CPP_DIR)/csv_row_counter

	# Build internal utilities
	g++ -O2 -std=c++17 $(UTILS_CPP_DIR)/schema_validator.cpp -o $(UTILS_CPP_DIR)/schema_validator
	g++ -O2 -std=c++17 $(UTILS_CPP_DIR)/ingestion_utils.cpp -o $(UTILS_CPP_DIR)/ingestion_utils

	@echo "[cpp-utils] Build complete: csv_row_counter (tests + pipeline), schema_validator, ingestion_utils"

cpp-schema: ## Build Stage 01 C++ schema validator
	@echo "[cpp-schema] Building Stage 01 C++ schema validator..."
	g++ -O2 -std=c++17 $(STAGE01_CPP_DIR)/cpp_schema_validator.cpp \
		-o $(STAGE01_CPP_DIR)/cpp_schema_validator
	@echo "[cpp-schema] Build complete."

cpp-all: cpp-schema cpp-utils ## Build all C++ binaries
	@echo "[cpp-all] All C++ binaries built."

# ==============================================================================
# Unified Build Target
# ==============================================================================

.PHONY: build
build: cpp-all lint ## Build C++ + lint Python
	@echo "[build] Build + lint complete."

# ==============================================================================
# Local CI — Mirrors GitHub Actions
# ==============================================================================

.PHONY: ci
ci: cpp-all python-tests lint ## Local CI pipeline
	@echo "[ci] Local CI pipeline complete."

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
	$(MAKE) -C deployment -f Makefile.deploy deploy
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
