import numpy as np
import roboticstoolbox as rtb

from robot_arm.dh import ARM, frames


def reference_robot():
    return rtb.DHRobot(
        [rtb.RevoluteDH(d=link.d, a=link.a, alpha=link.alpha, offset=link.offset) for link in ARM]
    )


def test_fk_matches_roboticstoolbox():
    rng = np.random.default_rng(0)
    robot = reference_robot()
    for _ in range(200):
        q = rng.uniform(-np.pi, np.pi, 6)
        np.testing.assert_allclose(frames(q)[-1], robot.fkine(q).A, atol=1e-12)


def test_home_pose_flange_position():
    # q = 0 (with the +pi/2 elbow offset) is the arm stretched horizontally along x at shoulder height.
    p = frames(np.zeros(6))[-1][:3, 3]
    np.testing.assert_allclose(p, [0.180 + 0.160 + 0.050, 0.0, 0.120], atol=1e-12)
