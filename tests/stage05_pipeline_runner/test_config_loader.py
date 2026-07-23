"""
Stage 05 — Test: Configuration Loader
================================================================================

This test verifies the behavior of load_pipeline_config():

- It loads valid YAML correctly
- It validates required Stage 05 fields
- It raises errors for missing or invalid configuration
- It raises errors for nonexistent config paths

All filesystem interactions use temporary directories for isolation.
"""

import pytest
import yaml

from src.stage05_pipeline_runner.config_loader import load_pipeline_config


# ------------------------------------------------------------------------------
# Test: Successful load of valid configuration
# ------------------------------------------------------------------------------
def test_config_loader_success(tmp_path):
    """Valid pipeline.yml should load correctly."""

    cfg_path = tmp_path / "pipeline.yml"
    cfg_path.write_text(yaml.dump({"stage05": {"output_dir": "data/stage05_reports"}}))

    cfg = load_pipeline_config(str(cfg_path))

    assert "stage05" in cfg
    assert cfg["stage05"]["output_dir"] == "data/stage05_reports"


# ------------------------------------------------------------------------------
# Test: Missing configuration file
# ------------------------------------------------------------------------------
def test_config_loader_missing_file(tmp_path):
    """Missing config file should raise FileNotFoundError."""

    missing_path = tmp_path / "does_not_exist.yml"

    with pytest.raises(FileNotFoundError):
        load_pipeline_config(str(missing_path))


# ------------------------------------------------------------------------------
# Test: Empty YAML file
# ------------------------------------------------------------------------------
def test_config_loader_empty_yaml(tmp_path):
    """Empty YAML should raise an exception."""

    cfg_path = tmp_path / "pipeline.yml"
    cfg_path.write_text("")  # empty file

    with pytest.raises(Exception):
        load_pipeline_config(str(cfg_path))


# ------------------------------------------------------------------------------
# Test: Missing stage05 section
# ------------------------------------------------------------------------------
def test_config_loader_missing_stage05(tmp_path):
    """Config missing 'stage05' section should raise an exception."""

    cfg_path = tmp_path / "pipeline.yml"
    cfg_path.write_text(yaml.dump({"stage02": {"foo": "bar"}}))

    with pytest.raises(Exception):
        load_pipeline_config(str(cfg_path))


# ------------------------------------------------------------------------------
# Test: Missing stage05.output_dir
# ------------------------------------------------------------------------------
def test_config_loader_missing_output_dir(tmp_path):
    """Config missing stage05.output_dir should raise an exception."""

    cfg_path = tmp_path / "pipeline.yml"
    cfg_path.write_text(yaml.dump({"stage05": {}}))

    with pytest.raises(Exception):
        load_pipeline_config(str(cfg_path))
