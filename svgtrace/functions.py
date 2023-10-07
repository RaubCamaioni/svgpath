from typing import List, Tuple
from math import pi, tau
import numpy as np

# https://en.wikipedia.org/wiki/B%C3%A9zier_curve
# https://stackoverflow.com/questions/197649/how-to-calculate-center-of-an-ellipse-by-two-points-and-radius-sizes
# https://en.wikipedia.org/wiki/List_of_trigonometric_identities#Product-to-sum_and_sum-to-product_identities


def cubic(
    p0: Tuple[float, float],
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    p3: Tuple[float, float],
    t: List[float],
) -> List[Tuple[float, float]]:
    t = t[:, np.newaxis]
    return (
        (1 - t) ** 3 * p0
        + 3 * (1 - t) ** 2 * t * p1
        + 3 * (1 - t) * t**2 * p2
        + t**3 * p3
    )


def quadratic(
    p0: Tuple[float, float],
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    t: List[float],
) -> List[Tuple[float, float]]:
    t = t[:, np.newaxis]
    return p1 + (1 - t) ** 2 * (p0 - p1) + t**2 * (p2 - p1)


def cw_ccw_difference(
    angle1: float,
    angle2: float,
) -> Tuple[float, float]:
    angle1 = angle1 % tau
    angle2 = angle2 % tau
    cw = (angle1 - angle2) % tau
    return -cw, tau - cw


def arc(
    p0: Tuple[float, float],
    d: Tuple[float, float],
    r: float,
    arc: bool,
    sweep: bool,
    p1: Tuple[float, float],
    t: List[float],
) -> List[Tuple[float, float]]:
    x0, y0 = p0
    a, b = d
    r = r * pi / 180
    x1, y1 = p1
    xd = x1 - x0
    yd = y1 - y0
    r0 = xd / (2 * a)
    r1 = yd / (2 * b)
    a0 = np.arctan2(-r0, r1) - r
    a1 = np.arcsin(min(np.sqrt(r0**2 + r1**2), 1)) - r

    w0 = a0 - a1
    w1 = a0 + a1

    w0s, w1s = w1 + pi, w0 + pi
    cw, ccw = cw_ccw_difference(w0, w1)
    cws, ccws = cw_ccw_difference(w0s, w1s)

    if sweep:
        d0 = ccw
        d1 = ccws
    else:
        d0 = cw
        d1 = cws

    if arc:
        sd = max(d0, d1, key=abs)
        w = w0 if abs(d0) > abs(d1) else w0s
    else:
        sd = min(d0, d1, key=abs)
        w = w0 if abs(d0) < abs(d1) else w0s

    def ellipse(w: float):
        return np.array(
            (
                a * np.cos(w + r),
                b * np.sin(w + r),
            )
        ).T

    return p0 + ellipse(w + sd * t) - ellipse(w)
