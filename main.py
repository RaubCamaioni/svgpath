import svg_peg
import svg_symbols
import svg_converter
import numpy as np
from matplotlib import pyplot as plt


def display_svg_path(svg_string: str):
    """display svg_paths with matplotlib"""

    tree = svg_peg.parse(svg_string)

    tokens = list(svg_symbols.tree_to_tokens(tree))
    abs_tokens = list(svg_converter.tokens_to_absolute(tokens))

    f = plt.figure("Absolute")
    for path in svg_symbols.tokens_to_path(abs_tokens, resolution=20):
        plt.plot(path[:, 0], -path[:, 1])
    plt.show()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type=str)
    args = parser.parse_args()

    with open(args.i, "r") as f:
        svg_string = f.read()

    display_svg_path(svg_string)
