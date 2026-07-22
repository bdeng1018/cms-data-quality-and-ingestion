"""
Stage 03 — Data Quality

This package provides baseline quality checks for raw POS/QIES data.
"""

from .quality_checks import QualityReport, run_quality_checks

__all__ = ["run_quality_checks", "QualityReport"]
