"""Standard Denavit-Hartenberg parameters (v2: homemade, ~0.40 m reach) and transforms."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class DHLink:
    d: float
    a: float
    alpha: float
    offset: float = 0.0  # added to the joint variable: theta = q + offset
    qlim: tuple[float, float] = (-np.pi, np.pi)


DEG = np.pi / 180

# Matches docs step 01 (v2). The forearm length lives in d4, not a3.
ARM: tuple[DHLink, ...] = (
    DHLink(d=0.120, a=0.0, alpha=+np.pi / 2, qlim=(-160 * DEG, 160 * DEG)),
    DHLink(d=0.0, a=0.180, alpha=0.0, qlim=(-10 * DEG, 170 * DEG)),
    DHLink(d=0.0, a=0.0, alpha=+np.pi / 2, offset=np.pi / 2, qlim=(-135 * DEG, 90 * DEG)),
    DHLink(d=0.160, a=0.0, alpha=-np.pi / 2, qlim=(-170 * DEG, 170 * DEG)),
    DHLink(d=0.0, a=0.0, alpha=+np.pi / 2, qlim=(-110 * DEG, 110 * DEG)),
    DHLink(d=0.050, a=0.0, alpha=0.0, qlim=(-180 * DEG, 180 * DEG)),
)


def dh_transform(theta: float, d: float, a: float, alpha: float) -> np.ndarray:
    """Homogeneous transform A_i^{i-1} for one standard-DH link."""
    ct, st = np.cos(theta), np.sin(theta)
    ca, sa = np.cos(alpha), np.sin(alpha)
    return np.array(
        [
            [ct, -st * ca, st * sa, a * ct],
            [st, ct * ca, -ct * sa, a * st],
            [0.0, sa, ca, d],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )


def frames(q: np.ndarray, links: tuple[DHLink, ...] = ARM) -> list[np.ndarray]:
    """Base frame plus every link frame: [T_0^0, T_1^0, ..., T_n^0]."""
    T = np.eye(4)
    out = [T]
    for qi, link in zip(q, links, strict=True):
        T = T @ dh_transform(qi + link.offset, link.d, link.a, link.alpha)
        out.append(T)
    return out
