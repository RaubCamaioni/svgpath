from matplotlib import pyplot as plt
from .symbols import tree_to_paths, tokens_to_trace
from .converter import paths_to_absolute_tokens
from . import peg


def display_svg_path(svg_string: str):
    """display svg_paths with matplotlib"""

    tree = peg.parse(svg_string)
    paths = tree_to_paths(tree)
    tokens = list(paths_to_absolute_tokens(paths))

    for t in tokens:
        print(t)

    _, ax = plt.subplots()
    ax.invert_yaxis()
    for trace in tokens_to_trace(tokens, resolution=100):
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
