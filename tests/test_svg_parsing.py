from pathlib import Path
import pytest
import svgpath

SVG_DIR = Path(__file__).parent / "resources" / "svgs"
SVG_FILES = sorted(SVG_DIR.glob("*.svg"))


@pytest.mark.parametrize("svg_file", SVG_FILES, ids=lambda p: p.name)
def test_parse_svg(svg_file, capsys):
    svg_string = svg_file.read_text()

    # tree parser: one entry per path element (d="..." attribute)
    tree = list(svgpath.parse(svg_string))
    n_tree = len(tree)

    # path parser: expand implicit repeated commands; 1:1 with tree entries
    paths = [list(p) for p in svgpath.tree_to_paths(tree)]
    n_paths = len(paths)
    n_path_tokens = sum(len(p) for p in paths)

    # absolute path parser: convert relative coords to absolute; 1:1 with paths
    abs_paths = [list(p) for p in svgpath.absolute_paths(iter(paths))]
    n_abs = len(abs_paths)
    n_abs_tokens = sum(len(p) for p in abs_paths)

    with capsys.disabled():
        print(f"\n{svg_file.name}")
        print(f"  tree paths:          {n_tree}")
        print(f"  expanded paths:      {n_paths}  ({n_path_tokens} tokens)")
        print(f"  absolute paths:      {n_abs}  ({n_abs_tokens} tokens)")

    assert n_tree > 0, f"no paths parsed from {svg_file.name}"
    assert n_paths == n_tree
    assert n_abs == n_paths
    assert n_path_tokens == n_abs_tokens
