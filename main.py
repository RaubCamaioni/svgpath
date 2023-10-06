import svg_peg
import svg_symbols
import numpy as np

if __name__ == "__main__":
    import argparse
    from matplotlib import pyplot as plt

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type=str)
    args = parser.parse_args()

    with open(args.i, "r") as f:
        svg_path = f.read()

    tree = svg_peg.parse(svg_path)
    tokens = svg_symbols.tree_to_tokens(tree)

    for p in tokens:
        print(p)

    for path in svg_symbols.tokens_to_path(tokens):
        plt.plot(path[:, 0], path[:, 1])
        plt.scatter(
            path[:, 0],
            path[:, 1],
            c=np.arange(len(path)),
            cmap="RdBu",
            marker="o",
            facecolors="none",
            linewidth=1,
        )

    plt.show()
