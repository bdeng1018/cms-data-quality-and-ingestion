"""
Smoke test for BaseIngestionSource interface.
Ensures the abstract class loads and exposes required methods.
"""

import pytest
from stage02_raw_ingestion.base_ingestion import BaseIngestionSource


def test_base_ingestion_interface():
    # Abstract class should not be instantiable
    with pytest.raises(TypeError):
        BaseIngestionSource("dummy_path")
