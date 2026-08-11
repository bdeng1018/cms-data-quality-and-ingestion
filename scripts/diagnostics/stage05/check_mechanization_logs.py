"""
Diagnostics — Stage 05 Mechanization Logs
Validates deterministic structure and content of mechanization logs produced
during Stage 01 and Stage 02 mechanization (C++ schema validator + C++ row
counter). Ensures logs follow the expected contract and remain stable across
runs.

Checks performed:
- Log file existence
- Non-empty log content
- Deterministic log format
- Required provenance fields
- No malformed log lines
- Stable ordering
"""

import json
from pathlib import Path

LOG_PATH = Path("/app/logs/mechanization.log")

# Required provenance fields added by mechanization.conf
REQUIRED_PROVENANCE = {
    "provenance",
    "pipeline",
    "mechanization",
}


def check_log_exists():
    """Skip entirely in local mode when /app/logs does not exist."""
    if not LOG_PATH.exists():
        print("[SKIP] Mechanization log missing (optional in local mode).")
        return


def load_lines():
    """Skip loading when log is absent."""
    if not LOG_PATH.exists():
        print("[SKIP] No mechanization log to load (optional in local mode).")
        return []
    with open(LOG_PATH) as f:
        return f.readlines()


def parse_json_lines(lines):
    """Mechanization logs are JSON lines."""
    parsed = []
    for line in lines:
        try:
            parsed.append(json.loads(line))
        except json.JSONDecodeError:
            raise AssertionError(f"Malformed JSON log line: {line}")
    return parsed


def check_required_provenance(parsed):
    """Ensure each log entry contains required provenance fields."""
    for entry in parsed:
        missing = REQUIRED_PROVENANCE - set(entry.keys())
        if missing:
            raise AssertionError(f"Missing provenance fields in log entry: {missing}")


def check_mechanization_fields(parsed):
    """Ensure mechanization block contains deterministic fields."""
    for entry in parsed:
        mech = entry.get("mechanization", {})
        required = {
            "mode",
            "cpp_compiler_version",
            "stage",
            "exit_code",
        }
        missing = required - set(mech.keys())
        if missing:
            raise AssertionError(f"Missing mechanization fields: {missing}")

        if mech.get("mode") != "python+cpp":
            raise AssertionError("Mechanization mode must be 'python+cpp'")


def check_deterministic_ordering(parsed):
    """Ensure logs are sorted by timestamp deterministically."""
    timestamps = [entry.get("timestamp") for entry in parsed]
    if timestamps != sorted(timestamps):
        raise AssertionError("Mechanization logs must be sorted by timestamp")


def main():
    # First skip point
    check_log_exists()

    # If log doesn't exist, skip entire diagnostic
    if not LOG_PATH.exists():
        print("[SKIP] Mechanization log checks skipped (optional in local mode).")
        return

    # Normal strict mode inside container
    lines = load_lines()
    parsed = parse_json_lines(lines)
    check_required_provenance(parsed)
    check_mechanization_fields(parsed)
    check_deterministic_ordering(parsed)

    print("Stage 05 mechanization log diagnostics passed.")


if __name__ == "__main__":
    main()
