"""
test_cpp_schema_validator.py
-----------------------------------------
Cross-language test for Stage 01 C++ schema validator.

Purpose:
    Ensure deterministic behavior of the compiled boundary validator.
    This test validates:
        - correct schema acceptance
        - correct rejection on column mismatch
        - stable error codes
        - reproducible output

Why this file exists:
    After adding a C++ boundary module, the next maturity step is
    proving integration through Python-based CI/CD testing.
"""

import subprocess
import tempfile
from pathlib import Path


def run_validator(schema_text: str, csv_text: str):
    """Helper to run the C++ validator deterministically."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        schema_file = tmp_path / "schema.txt"
        csv_file = tmp_path / "input.csv"

        schema_file.write_text(schema_text)
        csv_file.write_text(csv_text)

        BIN = (
            Path(__file__).resolve().parents[2]
            / "src/stage01_schema_definition/cpp_schema_validator"
        )

        result = subprocess.run(
            [str(BIN), str(schema_file), str(csv_file)], capture_output=True, text=True
        )

        return result.stdout.strip(), result.stderr.strip()


def test_valid_schema():
    schema = """id
facility_name
address
city
state
zip
"""
    csv = "id,facility_name,address,city,state,zip\n1,ABC,123 St,LA,CA,90001\n"

    stdout, stderr = run_validator(schema, csv)
    assert stdout == "VALID"
    assert stderr == ""


def test_column_count_mismatch():
    schema = """id
facility_name
address
city
state
zip
"""
    csv = "id,facility_name,address,city,state\n1,ABC,123 St,LA,CA\n"

    stdout, stderr = run_validator(schema, csv)
    assert stdout == ""
    assert stderr == "COLUMN_COUNT_MISMATCH"


def test_column_name_mismatch():
    schema = """id
facility_name
address
city
state
zip
"""
    csv = "id,facility_name,addr,city,state,zip\n1,ABC,123 St,LA,CA,90001\n"

    stdout, stderr = run_validator(schema, csv)
    assert stdout == ""
    assert stderr == "COLUMN_NAME_MISMATCH"


def test_empty_csv():
    schema = "id\nfacility_name\n"
    csv = ""

    stdout, stderr = run_validator(schema, csv)
    assert stdout == ""
    assert stderr == "EMPTY_CSV"


# ==============================================================================
# Deterministic behavior tests for C++ schema validator
# ==============================================================================


def test_deterministic_success_behavior():
    """Validator must behave deterministically on valid input."""
    schema = "id\nfacility_name\n"
    csv = "id,facility_name\n1,ABC\n"

    stdout1, stderr1 = run_validator(schema, csv)
    stdout2, stderr2 = run_validator(schema, csv)

    assert stdout1 == stdout2, "VALID stdout must be deterministic"
    assert stderr1 == stderr2, "stderr must be deterministic"
    assert stdout1 == "VALID", "Expected deterministic VALID output"
    assert stderr1 == "", "stderr must be empty on success"


def test_deterministic_failure_behavior():
    """Validator must behave deterministically on invalid input."""
    schema = "id\nfacility_name\n"
    csv = "id\n1\n"  # column mismatch

    stdout1, stderr1 = run_validator(schema, csv)
    stdout2, stderr2 = run_validator(schema, csv)

    # Deterministic behavior
    assert stdout1 == stdout2, "stdout must be deterministic"
    assert stderr1 == stderr2, "stderr must be deterministic"

    # Expected error token
    assert stdout1 == "", "stdout must be empty on failure"
    assert stderr1 == "COLUMN_COUNT_MISMATCH", "Expected COLUMN_COUNT_MISMATCH"


def test_error_message_formatting_is_stable():
    """Error messages must follow deterministic formatting rules."""
    schema = "id\nfacility_name\n"
    csv = ""  # empty CSV triggers E004

    stdout, stderr = run_validator(schema, csv)

    assert stdout == "", "Expected empty stdout for E004 error"
    assert stderr == "EMPTY_CSV", "Expected deterministic EMPTY_CSV error code"
    assert stdout.strip() == stdout, "stdout must not contain trailing whitespace"
    assert stderr.strip() == stderr, "stderr must not contain trailing whitespace"
    assert "\r" not in stdout, "stdout must not contain CR characters"
    assert "\r" not in stderr, "stderr must not contain CR characters"
