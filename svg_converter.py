from typing import Tuple, List, Dict
import numpy as np
from itertools import islice

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


def paths_to_absolute_tokens(paths: List[List[str]]):
    """return tokens in absolute format"""

    sm: Tuple[float, float] = np.array([0, 0])
    cp: Tuple[float, float] = np.array([0, 0])

    for tokens in paths:
        for token in tokens:
            c, args = token[0], np.array(token[1:], dtype=float)

            if c.islower():
                if c == "z":
                    pass
                elif c == "h":
                    cp = cp + [*args, 0]
                    args = [cp[0]]
                elif c == "v":
                    cp = cp + [0, *args]
                    args = [cp[1]]
                elif c == "m":
                    cp = cp + args
                    args = cp
                    sm = cp
                else:
                    args = args + (x_index[c] * cp[0]) + (y_index[c] * cp[1])
                    cp = args[-2:]
                if c == "z":
                    cp = sm
            else:
                if c == "M":
                    cp = args
                    sm = cp
                elif c == "Z":
                    cp = sm
                elif c == "H":
                    cp = np.array([args[0], cp[1]])
                elif c == "V":
                    cp = np.array([cp[0], args[0]])
                else:
                    cp = args[-2:]

            yield [c.upper(), *np.round(args, decimals=3).astype(str)]
