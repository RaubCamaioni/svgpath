from typing import Tuple, List, Dict, Generator
import numpy as np

x_index: Dict[str, int] = {
	'm': np.array([1, 0]),
	'l': np.array([1, 0]),
	'c': np.array([1, 0, 1, 0, 1, 0]),
	's': np.array([1, 0, 1, 0]),
	'q': np.array([1, 0, 1, 0]),
	't': np.array([1, 0]),
	'a': np.array([0, 0, 0, 0, 0, 1, 0]),
}

y_index: Dict[str, int] = {
	'm': np.array([0, 1]),
	'l': np.array([0, 1]),
	'c': np.array([0, 1, 0, 1, 0, 1]),
	's': np.array([0, 1, 0, 1]),
	'q': np.array([0, 1, 0, 1]),
	't': np.array([0, 1]),
	'a': np.array([0, 0, 0, 0, 0, 0, 1]),
}


def absolute_paths(
	paths: List[List[str]],
) -> Generator[List[str], None, None]:
	"""
	Convert relative tokens to absolute tokens.

	Args:
	    paths (List[List[str]]): Generator of svg tokens.

	Yields:
	    List[List[str]]: Generator of absolute svg tokens.
	"""

	def token_generator(tokens: List[List[str]]):
		closed_shape: Tuple[float, float] = np.array([0, 0])
		current_point: Tuple[float, float] = np.array([0, 0])

		for token in tokens:
			c = token[0]
			args = np.array(token[1:], dtype=float)

			if c.islower():
				if c == 'z':
					pass
				elif c == 'h':
					current_point = current_point + [*args, 0]
					args = [current_point[0]]
				elif c == 'v':
					current_point = current_point + [0, *args]
					args = [current_point[1]]
				elif c == 'm':
					current_point = current_point + args
					args = current_point
					closed_shape = current_point
				else:
					args = args + (x_index[c] * current_point[0]) + (y_index[c] * current_point[1])
					current_point = args[-2:]
				if c == 'z':
					current_point = closed_shape
			else:
				if c == 'M':
					current_point = args
					closed_shape = current_point
				elif c == 'Z':
					current_point = closed_shape
				elif c == 'H':
					current_point = np.array([args[0], current_point[1]])
				elif c == 'V':
					current_point = np.array([current_point[0], args[0]])
				else:
					current_point = args[-2:]

			yield [c.upper(), *np.round(args, decimals=3).astype(str).tolist()]

	for tokens in paths:
		yield token_generator(tokens)
