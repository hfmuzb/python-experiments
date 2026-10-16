"""Shared plot style matching codz.uz (dark, teal/amber, Source Code Pro) and arm drawing."""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

from robot_arm.dh import frames

BG = "#0a0a0a"
FG = "#e5e5e5"
MUTED = "#737373"
GRID = "#262626"
TEAL = "#00BFA6"
AMBER = "#F59E0B"
CYCLE = [TEAL, AMBER, "#60A5FA", "#F472B6", "#A3E635", "#C084FC"]


def _font() -> str:
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for name in ("Source Code Pro", "Menlo", "DejaVu Sans Mono"):
        if name in installed:
            return name
    return "monospace"


def use_style() -> None:
    mpl.rcParams.update(
        {
            "figure.facecolor": BG,
            "axes.facecolor": BG,
            "savefig.facecolor": BG,
            "axes.edgecolor": GRID,
            "axes.labelcolor": FG,
            "axes.titlecolor": FG,
            "axes.grid": True,
            "axes.axisbelow": True,
            "grid.color": GRID,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "text.color": FG,
            "legend.frameon": False,
            "axes.prop_cycle": mpl.cycler(color=CYCLE),
            "font.family": _font(),
            "font.size": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "lines.linewidth": 2,
            "figure.dpi": 110,
            "savefig.dpi": 200,
            "savefig.bbox": "tight",
        }
    )


def style_3d(ax) -> None:
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_pane_color((0, 0, 0, 0))
        axis._axinfo["grid"]["color"] = GRID
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_zlabel("z [m]")


def draw_arm(ax, q: np.ndarray, color: str = TEAL, alpha: float = 1.0, axes_len: float = 0.0):
    """Draw the arm as a polyline through joint origins; optionally draw each frame's axes."""
    Ts = frames(q)
    pts = np.array([T[:3, 3] for T in Ts])
    ax.plot(*pts.T, "-o", color=color, alpha=alpha, markersize=5, markerfacecolor=BG)
    if axes_len:
        for T in Ts:
            o = T[:3, 3]
            for k, c in zip(range(3), ("#ef4444", "#22c55e", "#3b82f6")):
                ax.quiver(*o, *(T[:3, k] * axes_len), color=c, linewidth=1)
    return pts


def save(fig, out_dir: Path, name: str) -> Path:
    """Save as PNG (200 dpi). The blog's media library doesn't accept SVG."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}.png"
    fig.savefig(path)
    plt.close(fig)
    return path
