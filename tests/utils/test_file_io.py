"""
test_file_io.py
-----------------------------------------
Deterministic tests for the ingestion-layer file I/O utilities.

This suite validates:
    - deterministic DataFrame → CSV writes (write_df)
    - deterministic CSV → DataFrame reads (read_csv)
    - UTF‑8 round‑trip correctness
    - correct FileNotFoundError propagation (ensure_exists)

These tests intentionally mirror the deterministic contract used across
Stages 01–04 of the CMS POS/QIES ingestion pipeline.
"""

from pathlib import Path

import pytest

from utils.file_io import ensure_exists, read_csv, write_df

TEST_DIR = Path("tmp/test_file_io")
TEST_FILE = TEST_DIR / "sample.csv"
MISSING_FILE = TEST_DIR / "missing.csv"


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Create and clean up the temporary test directory."""
    TEST_DIR.mkdir(parents=True, exist_ok=True)
    yield
    for f in TEST_DIR.iterdir():
        f.unlink()
    TEST_DIR.rmdir()


def test_write_df_deterministic():
    """write_df must produce identical output across repeated writes."""
    import pandas as pd

    df = pd.DataFrame({"col": ["hello", "world"]})
    write_df(df, TEST_FILE)
    first = TEST_FILE.read_text()

    write_df(df, TEST_FILE)
    second = TEST_FILE.read_text()

    assert first == second, "write_df() must be deterministic"


def test_read_csv_deterministic():
    """read_csv must return identical DataFrames across repeated reads."""
    import pandas as pd

    df = pd.DataFrame({"col": ["a", "b", "c"]})
    write_df(df, TEST_FILE)

    r1 = read_csv(TEST_FILE)
    r2 = read_csv(TEST_FILE)

    assert r1.equals(r2), "read_csv() must be deterministic"


def test_utf8_round_trip():
    """UTF‑8 content must round-trip correctly through write_df/read_csv."""
    import pandas as pd

    df = pd.DataFrame({"col": ["café", "naïve", "Διαγνωστικά"]})
    write_df(df, TEST_FILE)
    read_back = read_csv(TEST_FILE)

    assert read_back.equals(df), "UTF‑8 content must round-trip correctly"


def test_missing_file_raises():
    """ensure_exists must raise FileNotFoundError for missing files."""
    with pytest.raises(FileNotFoundError):
        ensure_exists(MISSING_FILE)
