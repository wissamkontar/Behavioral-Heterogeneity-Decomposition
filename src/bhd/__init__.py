"""
bhd — Behavioral Heterogeneity Decomposition.

Small helper package shared by the notebooks in this repository.
It provides (i) repository-relative paths, (ii) the publication plot
style used for every figure, and (iii) a clean reference implementation
of the two-shot common/personalized decomposition.

The notebooks keep the decomposition *inline* on purpose, so that each
figure of the paper can be reproduced from a single self-contained
notebook. `bhd.decomposition` is the same math, packaged for reuse.
"""

from .paths import ROOT_DIR, DATA_DIR, FIG_DIR
from .style import set_style
from .decomposition import (
    resample_to_grid,
    two_shot_decomposition,
    stack_trajectories,
    load_ngsim_stop_to_go,
)

__all__ = [
    "ROOT_DIR",
    "DATA_DIR",
    "FIG_DIR",
    "set_style",
    "resample_to_grid",
    "two_shot_decomposition",
    "stack_trajectories",
    "load_ngsim_stop_to_go",
]

__version__ = "1.0.0"
