import svg_peg
import svg_symbols
import svg_converter
import numpy as np
from matplotlib import pyplot as plt


def display_svg_path(svg_string: str):
    """display svg_paths with matplotlib"""

    tree = svg_peg.parse(svg_string)
    paths = svg_symbols.tree_to_paths(tree)
    tokens = list(svg_converter.paths_to_absolute_tokens(paths))

    for t in tokens:
        print(t)

    _, ax = plt.subplots()
    ax.invert_yaxis()
    for trace in svg_symbols.tokens_to_trace(tokens, resolution=100):
        ax.plot(trace[:, 0], trace[:, 1])
    plt.show()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type=str)
    args = parser.parse_args()

    with open(args.i, "r") as f:
        svg_string = f.read()

    display_svg_path(svg_string)
