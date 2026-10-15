# python-experiments

Code behind the articles on [codz.uz](https://codz.uz): visual experiments with Python and physics.

## Series: a $500 homemade 6-DOF robot arm

A mostly 3D-printed, stepper-driven arm (24 V, 100 g payload, ~0.40 m reach), built step by step. Each
article has its own folder with the draft and the script that regenerates every figure it uses.

| # | Article | Folder |
|---|---|---|
| 1 | Series intro: requirements, architecture, budget | `articles/robot-arm/01-…` |
| 2 | Kinematics: FK, IK, Jacobian, singularities | `articles/robot-arm/02-…` |
| 3 | Dynamics & torque sizing | `articles/robot-arm/03-…` |
| 4 | Trajectory planning | `articles/robot-arm/04-…` |
| … | Drivetrain, mechanics, electronics, firmware, software, calibration, validation | coming as the build progresses |

## Layout

```
src/robot_arm/        reusable library (DH model, kinematics, dynamics, trajectories, plot style)
tests/                pytest; cross-checks against roboticstoolbox-python
articles/robot-arm/   NN-slug/{article.mdx, make_figures.py, out/}
```

## Usage

```bash
uv sync                    # Python 3.12 + deps
uv run pytest              # tests
uv run make-figures 02     # regenerate figures for article 02 into its out/ folder
```
