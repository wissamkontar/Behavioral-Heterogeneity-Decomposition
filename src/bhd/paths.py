"""Repository-relative paths so notebooks run from any working directory."""

from pathlib import Path

# src/bhd/paths.py -> repository root is two levels up from this file's folder
ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
FIG_DIR = ROOT_DIR / "figures"

FIG_DIR.mkdir(parents=True, exist_ok=True)
