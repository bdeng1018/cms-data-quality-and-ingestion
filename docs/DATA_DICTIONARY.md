# Data Dictionary — Cleaned CMS POS/QIES Dataset

This document defines all columns in the canonical cleaned dataset produced by:

```code
data/stage02_cleaned/cleaned_data.csv
```

These fields represent the normalized output of the CMS **Provider of Services (POS)** ingestion and cleaning process.
Stage 01 regenerates `schema.json` from this dataset, and all downstream stages depend on these definitions.

All fields are treated as **strings** in Stage 01.

---

## 1. Facility Identification Fields

| Column | Type | Description | Notes |
| -------- | ------ | ------------- | ------- |
| `CROSS_REF_PROVIDER_NUMBER` | string | Cross-reference provider number | Optional |
| `PRVDR_NUM` | string | CMS provider number | Zero-padded; may contain mixed types |
| `LTC_CROSS_REF_PROVIDER_NUMBER` | string | Long-term care cross-reference | Optional |
| `PARENT_PROVIDER_NUMBER` | string | Parent provider number | Optional |
| `RELATED_PROVIDER_NUMBER` | string | Related provider number | Optional |
| `facility_id` | string | Primary facility identifier | Derived from POS `PRVDR_NUM`; normalized |

These identifiers form the backbone of facility‑level linkage across POS datasets.

---

## 2. Facility Location Fields

| Column | Type | Description | Notes |
| -------- | ------ | ------------- | ------- |
| `CITY_NAME` | string | City name | Mixed-type column; normalized to string |
| `SSA_CNTY_CD` | string | SSA county code | Mixed types |
| `STATE_CD` | string | Two-letter state code | May contain blanks |
| `SSA_STATE_CD` | string | SSA state code | Numeric or string |
| `STATE_RGN_CD` | string | State region code | Raw POS field |
| `ST_ADR` | string | Street address | Raw POS address field |
| `ZIP_CD` | string | ZIP code | Leading zeros preserved |
| `FIPS_STATE_CD` | string | FIPS state code | Optional |
| `FIPS_CNTY_CD` | string | FIPS county code | Optional |
| `CBSA_URBN_RRL_IND` | string | Urban/rural indicator | Optional |
| `CBSA_CD` | string | Core-based statistical area code | Optional |

These fields describe the facility’s physical location and federal geographic classifications.

---

## 3. Certification & Compliance Fields

| Column | Type | Description | Notes |
| -------- | ------ | ------------- | ------- |
| `CMPLNC_STUS_CD` | string | Compliance status code | optional |
| `CRTFCTN_DT` | string | Certification date | Numeric or blank |
| `ELGBLTY_SW` | string | Eligibility indicator | Y/N or blank |
| `ORGNL_PRTCPTN_DT` | string | Original participation date | Optional |
| `PGM_TRMNTN_CD` | string | Program termination code | Optional |
| `TRMNTN_EXPRTN_DT` | string | Termination expiration date | Optional |
| `CRTFCTN_ACTN_TYPE_CD` | string | Certification action type | Optional |
| `CRTFD_BED_CNT` | string | Certification-related field | Raw POS field |

These fields describe CMS certification, compliance, and participation history.

---

## 4. Provider Category & Type Fields

| Column | Type | Description | Notes |
| -------- | ------ | ------------- | ------- |
| `PRVDR_CTGRY_SBTYP_CD` | string | Provider subtype code | Optional |
| `PRVDR_CTGRY_CD` | string | Provider category code | Numeric or string |
| `GNRL_CNTL_TYPE_CD` | string | Control/ownership type | Optional |
| `GNRL_FAC_TYPE_CD` | string | General facility type | Optional |
| `NPP_TYPE_CD` | string | Non-physician provider type | Optional |

These fields classify the facility’s operational and ownership characteristics.

---

## 5. Change of Ownership (CHOW) Fields

| Column | Type | Description | Notes |
| -------- | ------ | ------------- | ------- |
| `CHOW_CNT` | string | Number of CHOW events | Numeric or blank |
| `CHOW_DT` | string | Most recent CHOW date | Optional |
| `CHOW_PRIOR_DT` | string | Prior CHOW date | Optional |
| `CHOW_SW` | string | CHOW indicator | Y/N |

These fields track ownership changes over time.

---

## 6. Intermediary Carrier Fields

| Column | Type | Description | Notes |
| -------- | ------ | ------------- | ------- |
| `INTRMDRY_CARR_CD` | string | Intermediary carrier code | Optional |
| `INTRMDRY_CARR_PRIOR_CD` | string | Prior intermediary carrier code | Optional |

---

## 7. Accreditation Fields

| Column | Type | Description | Notes |
| -------- | ------ | ------------- | ------- |
| `ACRDTN_EFCTV_DT` | string | Accreditation effective date | Optional |
| `ACRDTN_EXPRTN_DT` | string | Accreditation expiration date | Optional |
| `ACRDTN_TYPE_CD` | string | Accreditation type code | Optional |

---

## 8. Service Availability Fields (Hundreds of POS Service Codes)

These fields describe whether the facility provides specific services.

Examples include:

| Column | Type | Description | Notes |
| -------- | ------ | ------------- | ------- |
| `LAB_SRVC_CD` | string | Laboratory services | Categorical |
| `PHRMCY_SRVC_CD` | string | Pharmacy services | Categorical |
| `RDLGY_SRVC_CD` | string | Radiology services | Categorical |
| `ASC_BGN_SRVC_DT` | string | Ambulatory surgical center start date | Optional |
| `FREESTNDNG_ASC_SW` | string | Freestanding ASC indicator | Y/N |

There are **300+ service fields**, all treated as strings.

---

## 9. Bed Count & Unit Fields

| Column | Type | Description | Notes |
| -------- | ------ | ------------- | ------- |
| `CRTFD_BED_CNT` | string | Certified bed count | Numeric or blank |
| `ICFIID_BED_CNT` | string | ICF/IID bed count | Optional |
| `MDCD_NF_BED_CNT` | string | Medicaid NF bed count | Optional |
| `MDCR_SNF_BED_CNT` | string | Medicare SNF bed count | Optional |
| `BED_CNT` | string | Total bed count | Optional |
| `PSYCH_UNIT_BED_CNT` | string | Psychiatric unit bed count | Optional |
| `REHAB_UNIT_BED_CNT` | string | Rehab unit bed count | Optional |

These fields quantify facility capacity.

---

## 10. Staffing Fields

There are **150+ staffing fields**, all strings, representing counts of:

- RNs
- LPNs
- therapists
- aides
- contractors
- volunteers
- specialists

Examples:

| Column | Type | Description | Notes |
| -------- | ------ | ------------- | ------- |
| `RN_CNT` | string | Registered nurse count | Numeric or blank |
| `LPN_CNT` | string | Licensed practical nurse count | Numeric or blank |
| `PHYSN_CNT` | string | Physician count | Numeric or blank |
| `EMPLEE_CNT` | string | Total employee count | Numeric or blank |
| `VLNTR_CNT` | string | Volunteer count | Numeric or blank |

---

## 11. Miscellaneous POS Operational Fields

Examples:

| Column | Type | Description | Notes |
| -------- | ------ | ------------- | ------- |
| `SKLTN_REC_SW` | string | Skeleton record indicator | Y/N |
| `PHNE_NUM` | string | Phone number | Optional |
| `COLCTN_STUS_SW` | string | Collection status indicator | Y/N |
| `FAX_PHNE_NUM` | string | Fax number | Optional |
| `FY_END_MO_DAY_CD` | string | Fiscal year end code | Optional |

---

## 12. Notes on Data Types

- All fields are treated as **strings**
- Mixed-type columns are normalized to string
- Leading zeros are preserved
- Dates remain raw strings (no ISO normalization)
- Boolean-like fields (`Y/N`) remain strings

This matches Stage 01's deterministic schema contract.

---

## 13. Relationship to `schema.json`

Stage 01 regenerates:

```code
data/stage01_schema/schema.json
```

This dictionary corresponds directly to the fields in that schema.

If new fields are added or removed, both this file and `schema.json` must be updated together.

---

## 14. Contact

Maintainer: Brian Deng <br>
Email: <bdeng.data.pipelines@gmail.com> <br>
GitHub: <https://github.com/bdeng1018>
