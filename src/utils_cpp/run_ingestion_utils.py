"""
Utility wrapper for the C++ ingestion_utils binary.
Provides deterministic execution of Stage 05 ingestion utility modes
(normalize, delimiter, bom) and returns stdout for pipeline diagnostics.
"""

import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).parent / "ingestion_utils"


def run(mode: str) -> str:
    result = subprocess.run(
        [str(BIN), mode],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()


if __name__ == "__main__":
    print(run(sys.argv[1]))
