from .symbols import tree_to_paths, paths_to_points
from matplotlib import pyplot as plt
from . import peg
import warnings
import svgpath
import argparse


def display_svg_path(svg_string: str, no_clip: bool = False):
	"""display svg_paths with matplotlib"""

	tree = peg.parse(svg_string)
	# expanded to iterate with printer and plotter
	paths = [[token for token in path] for path in tree_to_paths(tree)]

	for i, path in enumerate(paths):
		print(f'Path: {i}')
		for tokens in path:
			print(f'  {tokens}')

	gen = paths_to_points(paths, resolution=20)
	points = [trace for paths in gen for trace in paths]

	_, ax = plt.subplots()

	ok, w, h = peg.parse_dimensions(svg_string)
	if ok and not no_clip:
		warnings.warn('svg viewbox clipping: render with --no-clip to show full paths')
		ax.set_xlim(0, w)
		ax.set_ylim(0, h)

	ax.invert_yaxis()

	for trace in points:
		ax.plot(trace[:, 0], trace[:, 1])

	plt.gca().set_aspect('equal')
	plt.show()


def plot():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', type=str)
	parser.add_argument('--no-clip', action='store_true')
	args = parser.parse_args()

	with open(args.i, 'r') as f:
		svg_string = f.read()

	display_svg_path(svg_string, args.no_clip)


def path():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', type=str)
	parser.add_argument('-a', action='store_true')
	args = parser.parse_args()

	with open(args.i, 'r') as f:
		svg_string = f.read()

	tree = svgpath.parse(svg_string)
	paths = svgpath.tree_to_paths(tree)

	if args.a:
		paths = svgpath.absolute_paths(paths)

	for i, path in enumerate(paths):
		print(f'Path: {i}')
		for token in path:
			print(f'  {token}')


def tree():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', type=str)
	args = parser.parse_args()

	with open(args.i, 'r') as f:
		svg_string = f.read()

	tree = svgpath.parse(svg_string)
	for path, start, end in tree:
		print(f'Path: {start}-{end}')
		for token in path:
			print('\t', token)
