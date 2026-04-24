# Loads maze levels from examples folder automatically.
# Each .txt file = one level
# Format: S = start, G = goal, # = wall, . = floor

from pathlib import Path

# Locate examples folder (one level above src/)
EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples"


def _load_file(path):
    """Read a level file and convert it to a grid."""
    with open(path, encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    return [list(line) for line in lines]


def _load_levels():
    """Load all level*.txt files in order."""
    files = sorted(EXAMPLES_DIR.glob("level*.txt"))

    if not files:
        raise FileNotFoundError("No level files found in examples/")

    return [_load_file(f) for f in files]


# Public variable used by the rest of the program
LEVELS = _load_levels()