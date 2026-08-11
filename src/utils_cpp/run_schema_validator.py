"""
Utility wrapper for the C++ schema validator.
Runs the compiled schema_validator binary against expected and actual
schema files, returning stdout deterministically for pipeline diagnostics.
"""

import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).parent / "schema_validator"


def run(expected: str, actual: str) -> str:
    result = subprocess.run(
        [str(BIN), expected, actual],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()


if __name__ == "__main__":
    print(run(sys.argv[1], sys.argv[2]))
