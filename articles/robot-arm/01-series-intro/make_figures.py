"""Article 1 (series intro): system architecture, DH frames, $500 budget."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from robot_arm.dh import DEG
from robot_arm.viz import AMBER, BG, FG, GRID, MUTED, TEAL, draw_arm, save, style_3d, use_style

OUT = Path(__file__).parent / "out"

BUDGET = {  # USD, AliExpress-level prices (docs step 04)
    "motors (6 steppers)": 75,
    "filament (~3 kg PETG)": 60,
    "bearings": 50,
    "aluminium / cnc parts": 50,
    "e-stop, wiring, cable chain": 40,
    "contingency": 40,
    "teensy 4.1": 32,
    "tmc2209 drivers": 30,
    "fasteners, inserts, pins": 30,
    "encoders + i2c mux": 25,
    "24 v psu": 25,
    "gt2 belts + pulleys": 25,
    "springs": 10,
    "gripper servo": 8,
}


def architecture():
    fig, ax = plt.subplots(figsize=(10, 4.9))
    ax.set_axis_off()
    ax.set(xlim=(0, 10), ylim=(0.7, 5.6))

    def box(x, y, w, h, text, color=TEAL):
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.02,rounding_size=0.08",
                facecolor=BG,
                edgecolor=color,
                linewidth=1.6,
            )
        )
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9, color=FG)

    def arrow(p, q, label="", color=MUTED, dy=0.15):
        ax.add_patch(
            FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=12, color=color, linewidth=1.3)
        )
        if label:
            ax.text(
                (p[0] + q[0]) / 2,
                (p[1] + q[1]) / 2 + dy,
                label,
                ha="center",
                fontsize=8,
                color=MUTED,
            )

    box(0.1, 2.9, 1.9, 1.1, "pc\npython host\nik + trajectories")
    box(3.0, 2.9, 1.9, 1.1, "teensy 4.1\nstep gen 1 khz\nencoder loop")
    box(6.0, 2.9, 1.7, 1.1, "6× tmc2209\nstepper drivers")
    box(8.3, 2.9, 1.6, 1.1, "6× steppers\nnema17/14/11")
    box(8.3, 0.9, 1.6, 1.1, "printed gears\ncycloidal / belt")
    box(6.0, 0.9, 1.7, 1.1, "6× as5600\njoint encoders")
    box(3.0, 0.9, 1.9, 1.1, "tca9548a\ni²c mux")
    box(6.0, 4.4, 1.7, 0.9, "24 v psu\n+ e-stop relay", color=AMBER)

    arrow((2.0, 3.45), (3.0, 3.45), "usb serial\n100–200 hz", dy=0.12)
    arrow((4.9, 3.45), (6.0, 3.45), "step / dir")
    arrow((7.7, 3.45), (8.3, 3.45))
    arrow((9.1, 2.9), (9.1, 2.0))
    arrow((8.3, 1.45), (7.7, 1.45), "magnet", dy=0.2)
    arrow((6.0, 1.45), (4.9, 1.45), "i²c")
    arrow((3.95, 2.0), (3.95, 2.9))
    ax.text(4.05, 2.4, "joint angles", fontsize=8, color=MUTED, va="center")
    arrow((6.85, 4.4), (6.85, 4.0), color=AMBER)
    ax.text(7.8, 4.85, "motor power,\ncut by e-stop", fontsize=8, color=AMBER, va="center")

    ax.set_title("system architecture", loc="left")
    return save(fig, OUT, "architecture")


def dh_frames():
    q = np.array([25, 55, -40, 0, -45, 0]) * DEG
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(projection="3d")
    pts = draw_arm(ax, q, axes_len=0.045)
    # Frames that share an origin (spherical wrist, coincident axes) get one combined label.
    groups = [
        ([0], "base"),
        ([1], "shoulder"),
        ([2, 3], "elbow"),
        ([4, 5], "wrist center"),
        ([6], "flange"),
    ]
    for idx, name in groups:
        p = pts[idx[0]]
        label = "{" + ",".join(map(str, idx)) + "}  " + name
        ax.text(*(p + [0.0, 0.0, 0.03]), label, fontsize=8, color=FG)
    style_3d(ax)
    ax.set_box_aspect((1, 1, 0.8))
    ax.set(xlim=(-0.1, 0.35), ylim=(-0.15, 0.3), zlim=(0, 0.36))
    ax.view_init(elev=22, azim=-60)
    ax.text2D(
        0.02,
        0.02,
        "x red · y green · z blue (z = joint axis)",
        transform=ax.transAxes,
        fontsize=8,
        color=MUTED,
    )
    ax.set_title("denavit–hartenberg frames {0}…{6}", loc="left")
    return save(fig, OUT, "dh-frames", fmt="png")


def budget():
    items = sorted(BUDGET.items(), key=lambda kv: kv[1])
    labels, values = zip(*items)
    total = sum(values)
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = [AMBER if lab == "contingency" else TEAL for lab in labels]
    ax.barh(labels, values, color=colors, height=0.65)
    for i, v in enumerate(values):
        ax.text(v + 1, i, f"${v}", va="center", fontsize=8, color=MUTED)
    ax.set_xlabel("usd")
    ax.grid(axis="y", visible=False)
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, 90)
    ax.set_title(f"where the ${total} goes", loc="left")
    for spine in ("left",):
        ax.spines[spine].set_color(GRID)
    return save(fig, OUT, "budget")


def main():
    use_style()
    for path in (architecture(), dh_frames(), budget()):
        print(path)


if __name__ == "__main__":
    main()
