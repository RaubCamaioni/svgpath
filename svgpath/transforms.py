from typing import List, Tuple
import numpy as np


def translate(
    x: float, y: float, points: List[List[Tuple[float, float]]]
) -> List[List[Tuple[float, float]]]:
    return [p + [x, y] for p in points]


def scale(
    x: float, y: float, points: List[List[Tuple[float, float]]]
) -> List[List[Tuple[float, float]]]:
    return [p * [x, y] for p in points]


def bounds(
    points: List[List[Tuple[float, float]]]
) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    points_stacked = np.concatenate(points, axis=0)
    minxy = np.min(points_stacked, axis=0)
    maxxy = np.max(points_stacked, axis=0)
    dimensions = maxxy - minxy
    center = minxy + dimensions / 2
    return *center, *dimensions
