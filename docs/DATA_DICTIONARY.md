# Data Dictionary — Cleaned CMS POS/QIES Dataset

This document defines all columns in the canonical cleaned dataset produced by:

```code
data/stage02_cleaned/cleaned_data.csv
```

These fields represent the unified, normalized output of the CMS POS/QIES ingestion and cleaning process.  
Stage 01 regenerates `schema.json` from this dataset, and all downstream stages depend on these definitions.

---

## 1. Facility Information

| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| `facility_id` | string | Unique identifier for the facility (POS/QIES) | Normalized to uppercase; no spaces |
| `facility_name` | string | Official facility name | Trimmed, de‑duplicated |
| `facility_type` | string | Facility classification (e.g., SNF, HHA, Hospice) | Derived from POS |
| `address_line1` | string | Facility street address | Cleaned for punctuation |
| `address_line2` | string | Additional address info | May be empty |
| `city` | string | City name | Title‑cased |
| `state` | string | Two‑letter state code | Always uppercase |
| `zip_code` | string | 5‑digit ZIP code | Leading zeros preserved |
| `county_name` | string | County name | Derived from QIES or POS |

---

## 2. Provider & Certification

| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| `provider_number` | string | CMS provider number | Zero‑padded to 6 digits |
| `ccn` | string | CMS Certification Number | Alias of provider_number if present |
| `npi` | string | National Provider Identifier | 10‑digit numeric; may be null |
| `ownership_type` | string | Ownership classification | Normalized categories |
| `medicare_certified` | boolean | Whether facility is Medicare‑certified | Derived from QIES |
| `medicaid_certified` | boolean | Whether facility is Medicaid‑certified | Derived from QIES |

---

## 3. Operational Status

| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| `operational_status` | string | Active / Closed / Pending | Normalized |
| `status_effective_date` | date | Date status became effective | ISO‑8601 format |
| `last_updated` | date | Last update timestamp from CMS source | ISO‑8601 format |

---

## 4. POS‑Specific Fields

| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| `pos_region` | string | CMS region code | Derived from POS |
| `pos_subregion` | string | Sub‑region classification | Optional |
| `pos_source_file` | string | Original POS file name | Useful for traceability |

---

## 5. QIES‑Specific Fields

| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| `qies_provider_category` | string | QIES provider category | Normalized |
| `qies_status_code` | string | QIES operational status code | Mapped to operational_status |
| `qies_source_file` | string | Original QIES file name | Useful for traceability |

---

## 6. Geocoding & Location Normalization

| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| `latitude` | float | Facility latitude | Derived from geocoding |
| `longitude` | float | Facility longitude | Derived from geocoding |
| `geocode_accuracy` | string | Rooftop / Range / Approximate | Optional |
| `fips_code` | string | County FIPS code | Derived from geocoding |

---

## 7. Cleaning & Normalization Flags

| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| `address_cleaned` | boolean | Whether address was normalized | True/False |
| `name_cleaned` | boolean | Whether facility name was normalized | True/False |
| `duplicate_flag` | boolean | Whether record was identified as a duplicate | Used in Stage 03 |
| `merge_source` | string | POS / QIES / Both | Indicates merge origin |

---

## 8. Quality & Validation Fields (Stage 03 Inputs)

| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| `schema_valid` | boolean | Whether record conforms to schema.json | Stage 03 input |
| `quality_score` | float | Composite quality score | Stage 03 output |
| `quality_flags` | string | Comma‑separated list of quality issues | Stage 03 output |

---

## 9. Notes on Data Types

- **Dates** are ISO‑8601 (`YYYY-MM-DD`)  
- **Booleans** are lowercase (`true` / `false`)  
- **Strings** are UTF‑8 normalized  
- **Floats** use decimal notation (no scientific notation)  
- **ZIP codes** remain strings to preserve leading zeros  

---

## 10. Relationship to `schema.json`

Stage 01 regenerates:

```code
data/stage01_schema/schema.json
```

This dictionary corresponds directly to the fields in that schema.  
If new fields are added or removed, both this file and `schema.json` must be updated together.

---

## 11. Contact

Maintainer: Brian Deng <br>
Email: <bdeng.data.pipelines@gmail.com> <br>  
GitHub: <https://github.com/bdeng1018>
