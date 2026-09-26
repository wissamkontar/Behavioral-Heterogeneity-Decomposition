#!/usr/bin/env python
"""
Execute every notebook in notebooks/ in order and regenerate all figures.

Usage (from the repository root):

    python scripts/run_all.py            # run all notebooks
    python scripts/run_all.py 05 09      # run only notebooks whose name starts with 05 or 09
    python scripts/run_all.py --inplace  # also save executed notebooks (with outputs) in place

Executed copies are written to notebooks/executed/ by default so that the
committed notebooks stay output-free. Figures are written to figures/.
"""

import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks"
EXEC_DIR = NB_DIR / "executed"


def main(argv):
    inplace = "--inplace" in argv
    prefixes = [a for a in argv if not a.startswith("--")]
    notebooks = sorted(p for p in NB_DIR.glob("*.ipynb") if not prefixes or any(p.name.startswith(x) for x in prefixes))
    if not notebooks:
        print("No notebooks matched.")
        return 1

    EXEC_DIR.mkdir(exist_ok=True)
    failures = []
    for nb_path in notebooks:
        t0 = time.time()
        print(f"→ {nb_path.name} ...", end=" ", flush=True)
        nb = nbformat.read(nb_path, as_version=4)
        client = NotebookClient(nb, timeout=1200, kernel_name="python3", resources={"metadata": {"path": str(NB_DIR)}})
        try:
            client.execute()
            out = nb_path if inplace else EXEC_DIR / nb_path.name
            nbformat.write(nb, out)
            print(f"ok ({time.time() - t0:.0f}s)")
        except Exception as exc:  # noqa: BLE001
            failures.append(nb_path.name)
            print(f"FAILED\n{exc}")

    n_fig = len(list((ROOT / "figures").glob("*.png")))
    print(f"\n{len(notebooks) - len(failures)}/{len(notebooks)} notebooks succeeded; {n_fig} figures in figures/")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
