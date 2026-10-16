"""Style sample: one 2D plot and one 3D arm drawing, to review the codz.uz look."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from robot_arm.dh import DEG
from robot_arm.viz import AMBER, MUTED, TEAL, draw_arm, save, style_3d, use_style

OUT = Path(__file__).parent / "out"


def quintic(t, T):
    s = t / T
    return 10 * s**3 - 15 * s**4 + 6 * s**5


def main():
    use_style()

    t = np.linspace(0, 2, 400)
    s = quintic(t, 2)
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.plot(t, s, label="position s(t)")
    ax.plot(t, np.gradient(s, t), label="velocity ṡ(t)")
    ax.set_xlabel("time [s]")
    ax.set_title("quintic rest-to-rest profile", loc="left")
    ax.legend()
    print(save(fig, OUT, "style-2d"))

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(projection="3d")
    draw_arm(ax, np.zeros(6), color=MUTED, alpha=0.5)
    draw_arm(ax, np.array([30, 45, -60, 0, 40, 0]) * DEG, color=TEAL, axes_len=0.04)
    draw_arm(ax, np.array([-50, 90, -30, 0, -30, 0]) * DEG, color=AMBER)
    style_3d(ax)
    ax.set_box_aspect((1, 1, 1))
    ax.set(xlim=(-0.4, 0.4), ylim=(-0.4, 0.4), zlim=(0, 0.5))
    ax.set_title("6-dof arm, three poses", loc="left")
    print(save(fig, OUT, "style-3d"))


if __name__ == "__main__":
    main()
