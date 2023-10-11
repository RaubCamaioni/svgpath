from typing import List, Tuple, Dict
from . import functions as svgf
import numpy as np

# token length lookup
arg_len: Dict[str, int] = {
    "m": 2,
    "l": 2,
    "h": 1,
    "v": 1,
    "c": 6,
    "s": 4,
    "q": 4,
    "t": 2,
    "a": 7,
    "z": 1,  # special case
}


def tree_to_paths(paths: List[List[str]]) -> List[List[str]]:
    """
    Expand SVG tokens into verbose format.

    Args:
        tree (List[List[str]]): List/Generator of SVG tokens.

    Returns:
        List[List[str]]: Generator of expanded SVG tokens paths.
    """

    def path_to_token(path):
        for token in path:
            l = arg_len[token[0].lower()]
            values = token[1:]
            et = [values[i * l : (i + 1) * l] for i in range(max(len(values), 1) // l)]
            for t in et:
                yield [token[0], *t]

    for path, start, end in paths:
        yield path_to_token(path)


def paths_to_points(
    paths: List[List[str]],
    resolution: int = 5,
) -> List[List[Tuple[float, float]]]:
    """
    SVG tokens to list of 2D points.

    Args:
        token (List[List[str]]): List/Generator of SVG tokens.
        resolution int: max number of points for each token.

    Returns:
        List[List[Tuple[float, float]]]: list of 2D points for each path
    """

    def path_to_points(path):
        s: Tuple[float, float] = np.array([0, 0])
        lm: Tuple[float, float] = np.array([0, 0])
        lcp: Tuple[float, float] = np.array([0, 0])
        tp: List[List[Tuple[float, float]]] = []
        t: List[float] = np.linspace(0, 1, resolution, endpoint=True)

        for p in path:
            c: str = p[0]
            cl = c.lower()
            args: List[str] = np.array(p[1:], dtype=float)

            if cl == "m":
                ns, points = move(c, s, args)
                lm = ns
                lcp = ns

            elif cl == "l":
                ns, points = line(c, s, args)
                lcp = ns

            elif cl == "h":
                ns, points = horizontal(c, s, args)
                lcp = ns

            elif cl == "v":
                ns, points = vertical(c, s, args)
                lcp = ns

            elif cl == "c":
                ns, points = cubic(c, s, args, t)

                if c.islower():
                    lcp = args[-4:-2] + s
                else:
                    lcp = args[-4:-2]

            elif cl == "s":
                ns, points = cubic_extended(c, s, lcp, args, t)

                if c.islower():
                    lcp = args[-4:-2] + s
                else:
                    lcp = args[-4:-2]

            elif cl == "q":
                ns, points = quadratic(c, s, args, t)

                if c.islower():
                    lcp = args[-4:-2] + s
                else:
                    lcp = args[-4:-2]

            elif cl == "t":
                ns, points = quadratic_extended(c, s, lcp, args, t)

                if c.islower():
                    lcp = args[-4:-2] + s
                else:
                    lcp = args[-4:-2]

            elif cl == "a":
                ns, points = arc(c, s, args, t)
                lcp = ns

            elif cl == "z":
                ns, points = close(s, lm)
                lcp = ns

            s = ns

            if len(points):
                tp.append(points)

            if (cl == "z" or cl == "m") and len(tp):
                yield np.vstack(tp)
                tp = []

        if len(tp):
            yield np.vstack(tp)

    for path in paths:
        yield path_to_points(path)


def move(
    c: str,
    s: Tuple[float, float],
    args: Tuple[float, float],
) -> Tuple[Tuple[float, float], List[Tuple[float, float]]]:
    if c.islower():
        e = s + args
    else:
        e = args
    return e, np.empty((0, 2), dtype=float)


def line(
    c: str,
    s: Tuple[float, float],
    args: Tuple[float, float],
) -> Tuple[Tuple[float, float], List[Tuple[float, float]]]:
    if c.islower():
        e = s + args
    else:
        e = args
    return e, np.array([s, e], dtype=float)


def horizontal(
    c: str,
    s: Tuple[float, float],
    args: List[float],
) -> Tuple[Tuple[float, float], List[Tuple[float, float]]]:
    if c.islower():
        e = s + [args[0], 0]
    else:
        e = np.array([args[0], s[1]])
    return e, np.array([s, e], dtype=float)


def vertical(
    c: str,
    s: Tuple[float, float],
    args: List[float],
) -> Tuple[Tuple[float, float], List[Tuple[float, float]]]:
    if c.islower():
        e = s + [0, args[0]]
    else:
        e = np.array([s[0], args[0]])
    return e, np.array([s, e], dtype=float)


def close(
    s: Tuple[float, float],
    args: Tuple[float, float],
) -> Tuple[Tuple[float, float], List[Tuple[float, float]]]:
    return args, np.array([s, args], dtype=float)


def cubic(
    c: str,
    s: Tuple[float, float],
    args: Tuple[float, float, float, float, float, float],
    t: List[float],
) -> Tuple[Tuple[float, float], List[Tuple[float, float]]]:
    p = np.array(args, dtype=float).reshape(-1, 2)
    if c.islower():
        p = p + s
    return p[-1], svgf.cubic(s, p[0], p[1], p[2], t)


def cubic_extended(
    c: str,
    s: Tuple[float, float],
    cp: Tuple[float, float],
    args: Tuple[float, float, float, float],
    t: List[float],
) -> Tuple[Tuple[float, float], List[Tuple[float, float]]]:
    p = np.array(args, dtype=float).reshape(-1, 2)
    if c.islower():
        p = p + s
    cp = 2 * s - cp
    return cubic("C", s, np.vstack((cp, p)), t)


def quadratic(
    c: str,
    s: Tuple[float, float],
    args: Tuple[float, float, float, float],
    t: List[float],
) -> Tuple[Tuple[float, float], List[Tuple[float, float]]]:
    p = np.array(args, dtype=float).reshape(-1, 2)
    if c.islower():
        p = p + s
    return p[-1], svgf.quadratic(s, p[0], p[1], t)


def quadratic_extended(
    c: str,
    s: Tuple[float, float],
    cp: Tuple[float, float],
    args: Tuple[float, float],
    t: List[float],
) -> Tuple[Tuple[float, float], List[Tuple[float, float]]]:
    p = np.array(args, dtype=float).reshape(-1, 2)
    if c.islower():
        p = p + s
    cp = 2 * s - cp
    return p[-1], cubic("Q", s, np.vstack((cp, p)), t)


def arc(
    c: str,
    s: Tuple[float, float],
    args: Tuple[float, float, float, float, float, float, float],
    t: List[float],
) -> Tuple[Tuple[float, float], List[Tuple[float, float]]]:
    d, r, arc, sweep, p1 = args[:2], args[2], args[3], args[4], args[5:7]
    if c.islower():
        p1 = p1 + s

    if np.linalg.norm(s - p1) > 0.0001:
        return p1, svgf.arc(s, d, r, arc, sweep, p1, t)
    else:
        return p1, np.empty((0, 2), dtype=float)
