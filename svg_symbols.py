from typing import List, Tuple, Dict
import numpy as np
import svg_functions as svgf


def truncate(input: str, length: int = 50) -> str:
    if len(input) > length:
        return input[: length - 3] + "..."
    else:
        return input


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
    "z": 1,
}


def tree_to_tokens(tree):
    """expands tokens with repeated arguments into verbose form"""
    tokens_expanded = []
    for tokens, start, end in tree:
        for token in tokens:
            l = arg_len[token[0].lower()]
            values = token[1:]
            expanded_tokens = [
                values[i * l : (i + 1) * l] for i in range(max(len(values), 1) // l)
            ]
            for expanded_token in expanded_tokens:
                tokens_expanded.append([token[0], *expanded_token])

    return tokens_expanded


def tokens_to_path(token: List[str], resolution: int = 5):
    s: Tuple[float, float] = np.array([0, 0])
    lm: Tuple[float, float] = np.array([0, 0])
    tp: List[List[Tuple[float, float]]] = []
    ttp: List = []
    t: List[float] = np.linspace(0, 1, resolution)

    for p in token:
        c = p[0]
        cl = c.lower()
        args = np.array(p[1:], dtype=float)

        if cl == "m":
            ns, points = move(c, s, args)
            lm = ns

        elif cl == "l":
            ns, points = line(c, s, args)

        elif cl == "h":
            ns, points = horizontal(c, s, args)

        elif cl == "v":
            ns, points = vertical(c, s, args)

        elif cl == "c":
            ns, points = cubic(c, s, args, t)
            if c.islower():
                lcp = args[-4:-2] + s

        elif cl == "s":
            ns, points = cubic_extended(c, s, lcp, args, t)
            if c.islower():
                lcp = args[-4:-2] + s

        elif cl == "q":
            ns, points = quadratic(c, s, args, t)
            if c.islower():
                lcp = args[-4:-2] + s

        elif cl == "t":
            ns, points = quadratic_extended(c, s, lcp, args, t)
            if c.islower():
                lcp = args[-4:-2] + s

        elif cl == "a":
            ns, points = arc(c, s, args, t)

        elif cl == "z":
            ns, points = close(s, lm)

        s = ns

        tp.append(points)

        if cl == "z" or cl == "m":
            ttp.append(np.vstack(tp))
            tp = []

    # if len(tp):
    #     ttp.append(np.vstack(tp))

    return ttp


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
        e = s + 0
        e[0] = args
    return e, np.array([s, e], dtype=float)


def vertical(
    c: str,
    s: Tuple[float, float],
    args: float,
) -> Tuple[Tuple[float, float], List[Tuple[float, float]]]:
    if c.islower():
        e = s + [0, args[0]]
    else:
        e = s + 0
        e[1] = args
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
    return p1, svgf.arc(s, d, r, arc, sweep, p1, t)
