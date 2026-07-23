"""
Stage 05 — Configuration Loader
================================================================================

This module loads the pipeline.yml configuration file for Stage 05 of the CMS
Data Quality & Ingestion Pipeline.

Responsibilities:
- Read YAML configuration from configs/pipeline.yml
- Validate required fields for Stage 05
- Return a Python dictionary consumed by run_pipeline.py and orchestrator.py

Stage 05 configuration is intentionally minimal to keep the control plane
predictable and deterministic.
"""

import os

import yaml


# ------------------------------------------------------------------------------
# Load pipeline configuration
# ------------------------------------------------------------------------------
def load_pipeline_config(config_path):
    """
    Load and validate the pipeline.yml configuration file.

    Parameters
    ----------
    config_path : str
        Path to configs/pipeline.yml

    Returns
    -------
    dict
        Parsed configuration dictionary

    Raises
    ------
    Exception
        If the file does not exist, cannot be parsed, or is missing required
        Stage 05 fields.
    """

    # --------------------------------------------------------------------------
    # Validate file existence
    # --------------------------------------------------------------------------
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    # --------------------------------------------------------------------------
    # Parse YAML
    # --------------------------------------------------------------------------
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        raise Exception(f"Failed to parse YAML config: {e}")

    if config is None:
        raise Exception("Configuration file is empty or invalid YAML.")

    # --------------------------------------------------------------------------
    # Validate Stage 05 fields
    # --------------------------------------------------------------------------
    if "stage05" not in config:
        raise Exception("Missing required 'stage05' section in pipeline.yml")

    stage05_cfg = config["stage05"]

    if "output_dir" not in stage05_cfg:
        raise Exception("Missing required field: stage05.output_dir")

    # --------------------------------------------------------------------------
    # Return parsed configuration
    # --------------------------------------------------------------------------
    return config
