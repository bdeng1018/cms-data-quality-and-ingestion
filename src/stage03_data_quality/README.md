# Stage 03 — Data Quality (Branch 1 MVP)

Stage 03 provides **baseline quality profiling** for raw POS/QIES data ingested in Stage 02.  
It does *not* clean, normalize, align, or enrich data.  
Its sole purpose is to compute lightweight quality metrics that help validate raw CMS files before transformation.

This stage is intentionally minimal for Branch 1.

---

## 📘 Overview

Stage 03 computes:

- row counts  
- null counts  
- duplicate counts  
- schema drift indicators  
- warnings for downstream diagnostics  

These metrics are returned as a structured `QualityReport` object and surfaced through a diagnostics script.

---

## 📂 File Layout

```text
src/
└── stage03_data_quality/
    ├── __init__.py
    └── quality_checks.py

scripts/
└── diagnostics/
    └── stage03/
        └── check_quality.py

tests/
└── stage03_data_quality/
    ├── test_quality_checks.py
    └── test_check_quality.py
```

---

## 🧠 Core Module — `quality_checks.py`

The core engine exposes:

- **[run_quality_checks](ca://s?q=Explain_stage_03_design)** — main entry point  
- `QualityReport` — dataclass containing structured metrics  
- helper functions for nulls, duplicates, drift  

This module is intentionally self‑contained and does not depend on domain logic or utilities.

---

## 🛠️ Diagnostics — `check_quality.py`

The diagnostics script:

- loads raw POS/QIES files from Stage 02  
- selects expected columns  
- runs quality checks  
- prints a human‑readable summary  
- writes results to `logs/quality.log`  

Example usage:

```bash
python scripts/diagnostics/stage03/check_quality.py \
    --file data/stage02_raw/pos_q2_2026.csv \
    --type pos
```

---

## 🧪 Tests

Two test files validate:

- engine correctness
- diagnostics execution
- log creation
- null/duplicate/drift behavior

Tests follow the same structure as Stage 01 and Stage 02.

---

## 📈 Expected Outputs

A typical `QualityReport` contains:

```text
row_count: 123456
null_counts: {"ccn": 0, "provider_type": 12, ...}
duplicate_counts: {"ccn": 45}
drift_indicators: {
    "missing_columns": [],
    "unexpected_columns": ["extra_col"]
}
warnings: [
    "Duplicate values detected in key column 'ccn'",
    "Unexpected columns present: ['extra_col']"
]
```

These metrics feed into Stage 04 reporting and Stage 05 orchestration.

---

## 🔧 Makefile Integration

Stage 03 is executed via:

```bash
make stage03
```

This target runs diagnostics and logs results.

---

## 🚀 Roadmap (Future Stages)

Stage 03 will expand in Branch 2+ to include:

- CCN validation
- facility normalization checks
- alignment rules
- cross‑dataset consistency

But Branch 1 remains intentionally lightweight.

---

## 🧭 Notes

Stage 03 is designed to be:

- simple
- testable
- reproducible
- consistent with Stage 01 + Stage 02

It provides the foundation for more advanced quality and validation layers in later branches.
