"""
Root-Level Pytest Configuration Helper
-----------------------------------------
Purpose:
    Pytest 9.x no longer honors the `pythonpath = src` directive in pytest.ini.
    This root-level conftest.py ensures that the ingestion pipeline's `src/`
    directory is always importable during test collection and execution.

Why this file exists:
    - Guarantees deterministic import behavior across:
        * local development
        * CI/CD runners
        * VS Code / PyCharm test explorers
        * Makefile-driven diagnostics
    - Prevents ModuleNotFoundError for imports such as:
        `from src.utils_cpp.run_csv_row_counter import ...`
    - Ensures test isolation: no reliance on external PYTHONPATH settings.

Design:
    - Insert project root and src/ into sys.path at highest priority.
    - Avoid side effects: no logging, no subprocess calls, no imports that
      execute pipeline code.
    - Deterministic resolution using pathlib rather than os.getcwd().

Notes:
    This file MUST be committed to version control. It is part of the test
    infrastructure and required for pytest 9.x compatibility with src/ layouts.
"""

import sys
from pathlib import Path

# Resolve project root deterministically
ROOT = Path(__file__).resolve().parent

# Resolve src/ directory relative to project root
SRC = ROOT / "src"

# ==============================================================================
# Import Path Injection (Pytest 9.x Compatible)
# ==============================================================================
# Insert src/ and project root at the beginning of sys.path.
# This ensures that Python resolves imports such as:
#     import src.utils_cpp.run_csv_row_counter
# regardless of the working directory from which pytest is invoked.
# ==============================================================================
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(ROOT))
