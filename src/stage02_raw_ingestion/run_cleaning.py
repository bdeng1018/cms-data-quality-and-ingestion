"""
Stage 02 — Raw POS/QIES Cleaning
================================================================================
Branch 1 cleaning module:
- Load raw POS parquet
- Normalize column names (raw → schema)
- Add metadata required by schema.json
- Enforce schema-driven dtypes
- Reindex to full schema (78 columns)
- Write cleaned_data.csv for Stage 03
"""

import os
from datetime import datetime

import pandas as pd

from src.stage01_schema_definition.schema_loader import load_schema
from utils.file_io import ensure_directory
from utils.logging_utils import get_logger

# ==============================================================================
# Configuration
# ==============================================================================
RAW_POS_PATH = "data/stage02_raw/pos_q2_2026.parquet"
OUTPUT_PATH = "data/stage02_cleaned/cleaned_data.csv"

logger = get_logger("stage02_cleaning")


# ==============================================================================
# COLUMN_MAP — Raw POS → Normalized Schema
# ==============================================================================
COLUMN_MAP = {
    # Identity
    "PRVDR_NUM": "facility_id",
    "PRVDR_NAME": "facility_name",
    "PRVDR_TYPE_CD": "facility_type",
    # Location
    "ADDR_LINE_1": "address_1",
    "ADDR_LINE_2": "address_2",
    "CITY_NAME": "city",
    "STATE_CD": "state",
    "ZIP_CD": "zip",
    "CNTY_NAME": "county",
    "SSA_CNTY_CD": "ssa_county_code",
    "STATE_RGN_CD": "state_region_code",
    "PRVNC_CD": "provider_region_code",
    # Ownership / Chain
    "GNRL_CTRL_TYPE_CD": "ownership_type",
    "CHN_AFLTN_CD": "chain_affiliation",
    "CORP_OWNER_NAME": "corporate_owner_name",
    "CORP_OWNER_ID": "corporate_owner_id",
    # Cross-reference
    "PARENT_PRVDR_NUM": "parent_facility_id",
    "RELATED_PRVDR_NUM": "related_facility_id",
    "CRS_REF_PRVDR_NUM": "cross_reference_provider_number",
    # NPP
    "NPP_TYPE_CD": "npp_type_code",
    # CLIA
    "CLIA_ID_1": "clia_id_1",
    "CLIA_ID_2": "clia_id_2",
    "CLIA_ID_3": "clia_id_3",
    "CLIA_ID_4": "clia_id_4",
    "CLIA_ID_5": "clia_id_5",
    # Operational flags
    "CAH_PSYCH_UNIT_SW": "cah_psych_unit_flag",
    "REHAB_UNIT_SW": "rehab_unit_flag",
    "SB_SW": "swing_bed_flag",
    "OVRRD_BED_CNT_SW": "override_bed_count_flag",
    "OVRRD_STFG_SW": "override_staffing_flag",
    # Participation flags
    "MDCD_MDCR_PRTCPTG_PRVDR_SW": "medicare_medicaid_participation_flag",
    "MEET_1861_SW": "meets_1861_flag",
    # Compliance / Waivers
    "COLCTN_STUS_SW": "collection_status_flag",
    "LSC_WVR_SW": "life_safety_code_waiver_flag",
    "RN_24_HR_WVR_SW": "rn_24_hour_waiver_flag",
    # Bed counts
    "BED_CNT_RPT": "bed_count_reported",
    "BED_CNT_CERT": "bed_count_certified",
    "BED_CNT_AVAIL": "bed_count_available",
    # Staffing (reported)
    "RN_HRS_RPT": "staffing_rn_hours_reported",
    "LPN_HRS_RPT": "staffing_lpn_hours_reported",
    "CNA_HRS_RPT": "staffing_cna_hours_reported",
    # Staffing (adjusted)
    "RN_HRS_ADJ": "staffing_rn_hours_adjusted",
    "LPN_HRS_ADJ": "staffing_lpn_hours_adjusted",
    "CNA_HRS_ADJ": "staffing_cna_hours_adjusted",
    # Emergency / Infection / Quality
    "EMERG_PREP_SW": "emergency_prep_plan_flag",
    "INF_CTRL_SW": "infection_control_flag",
    "QLTY_RPT_SW": "quality_reporting_flag",
    # Inspection / Penalties
    "INSPCTN_SCORE": "inspection_score",
    "INSPCTN_DATE": "inspection_date",
    "INSPCTN_RESULT": "inspection_result",
    "PNLTY_AMT": "penalty_amount",
    "PNLTY_DATE": "penalty_date",
    "PNLTY_REASON": "penalty_reason",
    # Five-star ratings
    "FIVE_STAR_OVERALL": "five_star_overall_rating",
    "FIVE_STAR_STAFFING": "five_star_staffing_rating",
    "FIVE_STAR_QUALITY": "five_star_quality_rating",
}


# ==============================================================================
# Dtype enforcement
# ==============================================================================
def enforce_dtypes(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    for field in schema["fields"]:
        col = field["name"]
        dtype = field["type"]

        if col not in df.columns:
            df[col] = None
            continue

        try:
            if dtype == "string":
                df[col] = df[col].astype("string")
            elif dtype == "integer":
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
            elif dtype == "float":
                df[col] = pd.to_numeric(df[col], errors="coerce")
            elif dtype == "boolean":
                df[col] = df[col].astype("boolean")
            elif dtype == "date":
                df[col] = pd.to_datetime(df[col], errors="coerce").dt.date
            elif dtype == "datetime":
                df[col] = pd.to_datetime(df[col], errors="coerce")
        except Exception as e:
            logger.warning(f"Failed dtype conversion for {col}: {e}")

    return df


# ==============================================================================
# Main cleaning function
# ==============================================================================
def run_stage02_cleaning():
    logger.info("Stage 02 cleaning started.")

    # Load raw POS
    df_raw = pd.read_parquet(RAW_POS_PATH)
    logger.info(f"Loaded raw POS data: {df_raw.shape}")

    # Normalize column names
    df = df_raw.rename(columns=COLUMN_MAP)

    # Load schema
    schema = load_schema()
    schema_cols = [f["name"] for f in schema["fields"]]

    # Add metadata BEFORE reindexing
    df["ingestion_source"] = "pos_q2_2026"
    df["ingestion_timestamp"] = datetime.utcnow()
    df["raw_file_quarter"] = "Q2"
    df["raw_file_year"] = 2026
    df["submission_timestamp"] = datetime.utcnow()

    # Enforce dtypes
    df = enforce_dtypes(df, schema)

    # Reindex to full schema (78 columns)
    df = df.reindex(columns=schema_cols)

    # Ensure output directory
    ensure_directory(os.path.dirname(OUTPUT_PATH))

    # Write cleaned output
    df.to_csv(OUTPUT_PATH, index=False)
    logger.info(f"Stage 02 cleaned data written to {OUTPUT_PATH}")

    return df


if __name__ == "__main__":
    run_stage02_cleaning()
