from matplotlib import pyplot as plt
from .symbols import tree_to_paths, paths_to_points
from . import peg
from .transforms import translate, scale, bounds
import numpy as np


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

    gen = paths_to_points(paths, resolution=20)
    points = [trace for paths in gen for trace in paths]

    x, y, w, h = bounds(points)
    points = translate(-x, -y, points)
    points = scale(1 / w, 1 / h, points)

    fig, ax = plt.subplots()
    ax.invert_yaxis()
    for trace in points:
        ax.plot(trace[:, 0], trace[:, 1])

        # plt.scatter(
        #     trace[:, 0],
        #     trace[:, 1],
        #     c=np.arange(len(trace)),
        #     cmap="RdBu",
        #     marker="o",
        #     facecolors="none",
        #     linewidth=1,
        # )

    plt.gca().set_aspect("equal")
    plt.show()


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type=str)
    args = parser.parse_args()

    with open(args.i, "r") as f:
        svg_string = f.read()

    display_svg_path(svg_string)


if __name__ == "__main__":
    main()
