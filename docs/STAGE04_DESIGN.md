# Stage 04 — Reporting Engine (v1.1.1)

Stage 04 transforms Stage 03 quality outputs into deterministic, contract‑aligned reporting artifacts.
It does **not** compute new quality metrics — instead, it enforces **reporting contracts**, validates structural completeness, and produces human‑readable summaries.

Stage 04 emits five artifacts:

- `dataset_summary.json` — dataset‑level reporting metrics
- `top_facilities.csv` — highest‑completeness facilities
- `bottom_facilities.csv` — lowest‑completeness facilities
- `sparse_columns.json` — columns violating reporting sparsity contract
- `column_health.json` — contract‑based column health classification

All outputs are deterministic, reproducible, and stable across repeated runs.

---

## 1. Reporting Model (v1.1.1)

Stage 04 consumes Stage 03 artifacts:

- `quality_summary.json`
- `facility_metrics.csv`
- `column_profiles.json`

and produces a **ReportingModel** containing:

### Required fields

- `total_rows`
- `total_facilities`
- `column_count`
- `dataset_quality`
- `dataset_completeness`
- `column_health_distribution`
- `warnings`

### v1.1.1 reporting fields

- `top_facilities`
- `bottom_facilities`
- `sparse_columns`
- `column_health` (per‑column contract evaluation)

These fields appear in Stage 04 artifacts and are validated by reporting diagnostics.

---

## 2. Stage 03 → Stage 04 Boundary (v1.1.1)

Stage 03 computes **quality**.
Stage 04 computes **reporting compliance**.

Key differences:

### Stage 03 (Quality)

- missingness
- sparsity
- null counts
- distinct counts
- quality_score
- facility completeness
- drift detection

### Stage 04 (Reporting)

- contract‑based column health
- reporting completeness (always 1.0 if artifacts generated)
- sparse column detection (contract‑based, not missingness‑based)
- top/bottom facility ranking
- dataset summary

This separation ensures deterministic reporting even when data is sparse.

---

## 3. Dataset Summary (v1.1.1)

`dataset_summary.json` contains:

- **Rows:** 44,707
- **Facilities:** 44,707
- **Columns:** 474
- **Dataset completeness:** 1.0
- **Dataset quality:** 0.1521687529
- **Warnings:** []

### Why completeness = 1.0?

Stage 04 completeness means:

> All reporting artifacts were successfully generated.

It does **not** refer to data completeness.

---

## 4. Column Health Contract (v1.1.1)

Stage 04 classifies each column as:

- `healthy`
- `moderate`
- `sparse`
- `critical`

### Real v1.1.1 results

- **Healthy:** 474
- **Moderate:** 0
- **Sparse:** 0
- **Critical:** 0

### Why all columns are healthy?

Stage 04 health is **contract‑based**, not missingness‑based.

A column is healthy if:

- dtype matches schema
- column exists
- metrics are structurally valid
- reporting contract is satisfied

Even columns with **100% nulls** can be healthy.

---

## 5. Sparse Column Detection (v1.1.1)

`sparse_columns.json` contains:

```code
[]
```

A column is sparse only if it violates the **reporting sparsity contract**, not if it has high missingness.

Examples of violations:

- wrong dtype
- missing required metadata
- structural inconsistency
- invalid metric shape

No columns violated the contract in v1.1.1.

---

## 6. Facility Ranking (v1.1.1)

Stage 04 ranks facilities by **completeness_score** from Stage 03.

### Top Facilities (Highest Completeness)

- **37.55% completeness:** 260197, 360039, 450099, 260065, 100015, 370028
- **37.34% completeness:** multiple facilities (150038, 190175, 370114, …)

### Bottom Facilities (Lowest Completeness)

- **5.49% completeness:** 751018, 661802, 391950, 751953, 034656
- **5.91% completeness:** multiple facilities (054667, 234631, 164607, …)

Ranking is deterministic and stable across runs.

---

## 7. Deterministic Artifact Contract

### `dataset_summary.json`

- keys sorted lexicographically
- deterministic values
- includes v1.1.1 reporting fields

### `top_facilities.csv` / `bottom_facilities.csv`

- deterministic ordering
- stable completeness_score ranking

### `sparse_columns.json`

- deterministic list
- empty in v1.1.1

### `column_health.json`

- lexicographically sorted keys
- deterministic contract evaluation
- includes dtype notes (e.g., “dtype may be inconsistent”)

---

## 8. Diagnostics Contract (v1.1.1)

Stage 04 diagnostics validate:

- artifact existence
- deterministic ordering
- required reporting fields
- column health contract
- sparse column contract
- facility ranking determinism
- dataset summary consistency

Diagnostics ensure Stage 04 artifacts are structurally valid and reproducible.

---

## 9. Release Contract (v1.1.1)

The Stage 04 release manifest includes:

- reporting completeness
- column health distribution
- sparse column list
- facility ranking metadata
- deterministic ordering guarantees
- updated artifact paths

This ensures reproducibility and traceability across pipeline versions.

---

## 10. Contact

Maintainer: Brian Deng  <br>
Email: <bdeng.data.pipelines@gmail.com>  <br>
GitHub: <https://github.com/bdeng1018>
