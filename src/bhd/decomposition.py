"""
Two-shot common / personalized decomposition of behavioral trajectories.

Given a matrix ``X`` of shape ``(T, N)`` holding ``N`` agent trajectories
sampled on a common grid of ``T`` points, the behavior of agent *v* is
modeled as

    x_v  ≈  C Ψ_v  +  P_v Φ_v

where

* ``C``   (T × k_c) is a *common* basis shared by every agent, with agent
  scores ``Ψ`` (k_c × N);
* ``P_v`` (T × k_p) is a *personalized* basis that belongs to agent *v*
  alone, with scores ``Φ_v``.

The "two-shot" estimator used throughout the paper is:

1. **Shot 1 — common component.** PCA across agents (each agent is one
   sample, each time step one feature) yields ``C``; ``Ψ = Cᵀ X``.
2. **Shot 2 — personalized component.** For each agent, PCA on its own
   residual ``r_v = x_v − C Ψ_v`` yields ``P_v, Φ_v``.

This module is a packaged, documented version of the inline code found
in every notebook. The notebooks keep the inline version so that each
figure in the paper is reproducible from one self-contained file.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA


# --------------------------------------------------------------------- #
# Pre-processing
# --------------------------------------------------------------------- #
def resample_to_grid(values: np.ndarray, n_points: int) -> np.ndarray:
    """Linearly resample a 1-D series onto ``n_points`` on [0, 1].

    This is the *context alignment* step: trajectories of different
    duration are mapped to the same normalized-time grid so they can be
    stacked column-wise.
    """
    values = np.asarray(values, dtype=float)
    return np.interp(
        np.linspace(0.0, 1.0, n_points),
        np.linspace(0.0, 1.0, len(values)),
        values,
    )


def stack_trajectories(
    df: pd.DataFrame,
    id_col: str,
    value_col: str,
    n_points: int | None = None,
    min_samples: int = 0,
    max_agents: int | None = None,
) -> tuple[np.ndarray, list]:
    """Build the ``(T, N)`` trajectory matrix from a long-format DataFrame.

    Parameters
    ----------
    df : DataFrame in long format (one row per agent per time step).
    id_col : column identifying the agent.
    value_col : column holding the behavioral signal (speed, accel, ...).
    n_points : length of the common grid. Defaults to the shortest
        trajectory (the paper's choice for NGSIM) — pass e.g. 200 to use
        a fixed grid (the paper's choice for TGSIM).
    min_samples : drop agents with fewer raw samples than this.
    max_agents : optionally keep only the first ``max_agents`` ids
        (after sorting), as done for some visualizations.

    Returns
    -------
    X : ndarray, shape (T, N)
    ids : list of the agent ids in column order
    """
    counts = df[id_col].value_counts()
    ids = sorted(counts[counts > min_samples].index.tolist())
    if max_agents is not None:
        ids = ids[:max_agents]
    if n_points is None:
        n_points = int(counts.loc[ids].min())

    cols = [resample_to_grid(df.loc[df[id_col] == i, value_col].values, n_points) for i in ids]
    return np.stack(cols, axis=1), ids


# --------------------------------------------------------------------- #
# Core estimator
# --------------------------------------------------------------------- #
def two_shot_decomposition(
    X: np.ndarray,
    n_common: int = 1,
    n_personal: int = 1,
    force_positive: bool = False,
) -> dict:
    """Two-shot common/personalized decomposition.

    Parameters
    ----------
    X : ndarray, shape (T, N). Columns are agents.
    n_common : number of shared components ``k_c``.
    n_personal : number of personalized components ``k_p`` per agent.
    force_positive : if True, clip the reconstruction at zero and
        re-derive the personalized part from the clipped reconstruction.
        Used for physically non-negative signals (spacing, speed).

    Returns
    -------
    dict with keys
        ``C``            (T, k_c)  common basis
        ``Psi``          (k_c, N)  common scores
        ``shared``       (T, N)    C Ψ
        ``personal``     (T, N)    P_v Φ_v for every agent
        ``reconstructed``(T, N)    shared + personal
    """
    X = np.asarray(X, dtype=float)
    T, N = X.shape

    # ---- Shot 1: common component (PCA across agents) --------------- #
    pca_shared = PCA(n_components=n_common)
    C = pca_shared.fit(X.T).components_.T  # (T, k_c)
    Psi = C.T @ X  # (k_c, N)
    shared = C @ Psi  # (T, N)

    # ---- Shot 2: per-agent PCA on the residual ---------------------- #
    personal = np.empty_like(X)
    for v in range(N):
        r_v = (X[:, v] - shared[:, v]).reshape(-1, 1)
        pca_personal = PCA(n_components=n_personal)
        phi_v = pca_personal.fit_transform(r_v)
        personal[:, v] = pca_personal.inverse_transform(phi_v).ravel()

    reconstructed = shared + personal
    if force_positive:
        reconstructed = np.clip(reconstructed, 0.0, None)
        personal = np.clip(reconstructed - shared, 0.0, None)

    return {
        "C": C,
        "Psi": Psi,
        "shared": shared,
        "personal": personal,
        "reconstructed": reconstructed,
    }


# --------------------------------------------------------------------- #
# Data loaders
# --------------------------------------------------------------------- #
NGSIM_COLUMNS = [
    "time",
    "leader_pos",
    "follower_pos",
    "leader_speed",
    "follower_speed",
    "leader_acc",
    "follower_acc",
    "trajectory_id",
    "spacing",
]


def load_ngsim_stop_to_go(path) -> pd.DataFrame:
    """Load ``data/ngsim/stop_to_go.csv`` with clean column names.

    The raw file has a header row and nine columns; the last one is the
    pre-computed spacing (leader − follower position). All columns are
    coerced to numeric and rows with missing values are dropped.
    """
    df = pd.read_csv(path, header=0)
    df.columns = NGSIM_COLUMNS[: df.shape[1]]
    df = df.apply(pd.to_numeric, errors="coerce").dropna()
    df["spacing"] = df["leader_pos"] - df["follower_pos"]
    return df
