"""Publication plot style shared by all notebooks.

The paper figures use Times New Roman. On machines without that font
(most Linux boxes), matplotlib silently falls back to the next serif
font in the list below, so the notebooks still run without warnings.
"""

import matplotlib.pyplot as plt

FONT_TITLE = 22
FONT_LABEL = 22
FONT_TICK = 20
FONT_LEGEND = 18


def set_style(seaborn_white: bool = False) -> None:
    """Apply the paper's matplotlib style.

    Parameters
    ----------
    seaborn_white : bool
        If True, also apply ``seaborn.set_style("white")`` (used by the
        real-data notebooks).
    """
    if seaborn_white:
        import seaborn as sns

        sns.set_style("white")

    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = [
        "Times New Roman",
        "Times",
        "Nimbus Roman",
        "Liberation Serif",
        "DejaVu Serif",
    ]
    plt.rcParams["mathtext.fontset"] = "cm"
    plt.rcParams["savefig.dpi"] = 300
    plt.rcParams["savefig.bbox"] = "tight"
