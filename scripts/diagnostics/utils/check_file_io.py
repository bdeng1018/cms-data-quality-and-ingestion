"""
Diagnostics — Utils: file_io.py
Validates deterministic behavior of the file_io utility module. Ensures stable
read/write operations, UTF‑8 consistency, newline normalization, and correct
error propagation.

Checks performed:
- Module importability
- Deterministic write_file() behavior
- Deterministic read_file() behavior
- UTF‑8 encoding consistency
- Newline normalization
- Correct error handling for missing files
"""

from pathlib import Path

from utils.file_io import read_file, write_file

TEST_DIR = Path("tmp/diagnostics_file_io")
TEST_FILE = TEST_DIR / "test.txt"
MISSING_FILE = TEST_DIR / "missing.txt"


def setup_test_dir():
    TEST_DIR.mkdir(parents=True, exist_ok=True)


def cleanup_test_dir():
    if TEST_DIR.exists():
        for f in TEST_DIR.iterdir():
            f.unlink()
        TEST_DIR.rmdir()


def check_write_file_deterministic():
    """Ensure write_file() produces deterministic output."""
    content = "hello\nworld\nthis is deterministic\n"

    write_file(TEST_FILE, content)
    first = TEST_FILE.read_text()

    write_file(TEST_FILE, content)
    second = TEST_FILE.read_text()

    if first != second:
        raise AssertionError("write_file() produced non-deterministic output")


def check_read_file_deterministic():
    """Ensure read_file() returns deterministic content."""
    content = "line1\nline2\nline3\n"
    write_file(TEST_FILE, content)

    r1 = read_file(TEST_FILE)
    r2 = read_file(TEST_FILE)

    if r1 != r2:
        raise AssertionError("read_file() produced non-deterministic output")


def check_utf8_consistency():
    """Ensure UTF‑8 encoding is preserved."""
    content = "café\nnaïve\nΔιαγνωστικά\n"
    write_file(TEST_FILE, content)

    read_back = read_file(TEST_FILE)
    if read_back != content:
        raise AssertionError("UTF‑8 content mismatch in file_io")


def check_newline_normalization():
    """Ensure newline normalization is deterministic."""
    content = "a\r\nb\r\nc\r\n"
    write_file(TEST_FILE, content)

    read_back = read_file(TEST_FILE)
    if "\r" in read_back:
        raise AssertionError("Newline normalization failed (CR detected)")


def check_missing_file_error():
    """Ensure missing files raise deterministic exceptions."""
    try:
        read_file(MISSING_FILE)
    except FileNotFoundError:
        return
    except Exception as e:
        raise AssertionError(f"Unexpected exception for missing file: {e}")

    raise AssertionError("read_file() did not raise FileNotFoundError for missing file")


def main():
    setup_test_dir()
    try:
        check_write_file_deterministic()
        check_read_file_deterministic()
        check_utf8_consistency()
        check_newline_normalization()
        check_missing_file_error()
        print("Utils file_io diagnostics passed.")
    finally:
        cleanup_test_dir()


if __name__ == "__main__":
    main()
