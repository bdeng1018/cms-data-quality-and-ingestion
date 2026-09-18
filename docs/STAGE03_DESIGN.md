# Stage 03 — Data Quality Engine (v1.1.1)

Stage 03 performs deterministic, schema‑aligned quality validation on the Stage 02 cleaned dataset.
It produces three intermediate artifacts:

- `quality_summary.json` — dataset‑level metrics
- `facility_metrics.csv` — facility‑level metrics
- `column_profiles.json` — column‑level metrics

All outputs are deterministic, reproducible, and stable across repeated runs.

---

## 1. QualityReport Structure (v1.1.1)

Stage 03 computes a `QualityReport` object containing:

### Required fields

- `row_count` — total rows (44,707 in v1.1.1)
- `null_counts` — per‑column null counts
- `duplicate_counts` — duplicate row detection
- `drift_indicators` — schema drift signals
- `warnings` — deterministic warning list

### New v1.1.1 fields

Stage 03 now includes completeness and metadata completeness invariants:

- `missing_required_columns`
- `empty_required_columns`
- `missing_metadata_fields`
- `metadata_fields_with_nulls`
- `drift_severity` (`none`, `minor`, `major`)

These fields appear in `quality_summary.json` when present and are validated by Stage 03 diagnostics.

---

## 2. Completeness Invariants (v1.1.1)

Completeness validation ensures structural integrity of the dataset.

### Required completeness

A column is considered required if defined in the Stage 01 schema.

- Missing required columns → `missing_required_columns`
- Required columns present but fully null → `empty_required_columns`

### Metadata completeness

Metadata fields (e.g., facility name, state, ZIP) are validated separately:

- Missing metadata fields → `missing_metadata_fields`
- Metadata fields containing nulls → `metadata_fields_with_nulls`

These invariants ensure downstream reporting receives structurally complete data.

---

## 3. Schema Drift Detection (v1.1.1)

Stage 03 detects schema drift relative to Stage 01:

- `missing_columns` — expected columns not present
- `unexpected_columns` — columns not defined in schema
- `drift_severity` — deterministic classification:
  - `none`
  - `minor`
  - `major`

Drift severity is included in `quality_summary.json` and validated by diagnostics.

---

## 4. Deterministic Warning System (v1.1.1)

Stage 03 produces a deterministic list of warnings:

- duplicate rows
- missing required columns
- empty required columns
- missing metadata fields
- metadata fields with nulls
- schema drift
- unexpected columns

Warnings are sorted lexicographically to guarantee reproducibility.

---

## 5. Deterministic Artifact Contract

### `quality_summary.json`

- Keys sorted lexicographically
- Includes optional v1.1.1 fields when present
- Deterministic across repeated runs
- Contains real v1.1.1 metrics:
  - `column_count = 474`
  - `facility_count = 44,707`
  - `overall_quality_score = 0.1521687529`

### `facility_metrics.csv`

- Fixed column order:
  - `facility_id`
  - `row_count`
  - `missingness_rate`
  - `quality_score`
- Deterministic row ordering
- Real v1.1.1 ranges:
  - typical completeness: **6–7%**
  - top facilities: **~35–37.5%**
  - bottom facilities: **~5.5–6%**

### `column_profiles.json`

- Columns sorted lexicographically
- Metrics sorted lexicographically
- Deterministic across repeated runs
- Real v1.1.1 patterns:
  - fully missing columns (null_count = 44,707)
  - highly sparse columns (null_count ≈ 31k–33k)
  - moderate sparsity (null_count ≈ 18k)
  - fully complete columns (null_count = 0)

---

## 6. Diagnostics Contract (v1.1.1)

Stage 03 diagnostics validate:

- artifact existence
- deterministic ordering
- required fields
- optional completeness fields
- schema alignment
- warning list determinism

Completeness and metadata completeness fields are validated in optional mode to support partial development runs.

---

## 7. Release Contract (v1.1.1)

The Stage 03 release manifest includes:

- completeness invariants
- metadata completeness invariants
- drift severity
- deterministic ordering guarantees
- updated artifact paths

This ensures reproducibility and traceability across pipeline versions.

---

## 8. Contact

Maintainer: Brian Deng  <br>
Email: <bdeng.data.pipelines@gmail.com>  <br>
GitHub: <https://github.com/bdeng1018>
