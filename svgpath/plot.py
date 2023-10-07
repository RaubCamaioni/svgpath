from matplotlib import pyplot as plt
from .symbols import tree_to_paths, paths_to_points
from . import peg


def display_svg_path(svg_string: str):
    """display svg_paths with matplotlib"""

    tree = peg.parse(svg_string)
    # expanded to iterate with printer and plotter
    paths = [[token for token in path] for path in tree_to_paths(tree)]

    for i, path in enumerate(paths):
        print(f"Path: {i}")
        for tokens in paths:
            for token in tokens:
                print(f"  {token}")

    _, ax = plt.subplots()
    ax.invert_yaxis()  # origin at top left
    for path in paths_to_points(paths, resolution=100):
        for trace in path:
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
