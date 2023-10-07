from typing import Tuple, List, Dict
import numpy as np

x_index: Dict[str, int] = {
    "m": np.array([1, 0]),
    "l": np.array([1, 0]),
    "c": np.array([1, 0, 1, 0, 1, 0]),
    "s": np.array([1, 0, 1, 0]),
    "q": np.array([1, 0, 1, 0]),
    "t": np.array([1, 0]),
    "a": np.array([0, 0, 0, 0, 0, 1, 0]),
}

y_index: Dict[str, int] = {
    "m": np.array([0, 1]),
    "l": np.array([0, 1]),
    "c": np.array([0, 1, 0, 1, 0, 1]),
    "s": np.array([0, 1, 0, 1]),
    "q": np.array([0, 1, 0, 1]),
    "t": np.array([0, 1]),
    "a": np.array([0, 0, 0, 0, 0, 0, 1]),
}


def tokens_to_absolute(tokens: List[List[str]]):
    """return tokens in absolute format"""
    lm: Tuple[float, float] = np.array([0, 0])
    cp: Tuple[float, float] = np.array([0, 0])

    for token in tokens:
        c, args = token[0], np.array(token[1:], dtype=float)
        cl = c.lower()

        if c.islower():
            if cl == "z":
                pass
            elif cl == "h":
                cp = cp + [*args, 0]
                args = [cp[0]]
            elif cl == "v":
                cp = cp + [0, *args]
                args = [cp[1]]
            else:
                args = args + (x_index[cl] * cp[0]) + (y_index[cl] * cp[1])
                cp = args[-2:]
            if cl == "m":
                lm = cp
            elif cl == "z":
                cp = lm
        else:
            if c == "M":
                cp = args
                lm = cp
            elif c == "Z":
                cp = lm
            elif c == "H":
                cp = np.array([args[0], cp[1]])
            elif c == "V":
                cp = np.array([cp[0], args[0]])
            else:
                cp = args[-2:]

        yield [c.upper(), *np.round(args, decimals=3).astype(str)]
