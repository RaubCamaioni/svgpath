from typing import Optional as TypingOptional, Tuple, List
from pyparsing import (
	Word,
	Literal,
	nums,
	Combine,
	Optional,
	Suppress,
	OneOrMore,
	ZeroOrMore,
	Or,
	Group,
)


def Caseless(c: str):
	return Literal(c.lower()) | Literal(c.upper())


number_integer = Word(nums)
number_float = Word(nums) + Literal('.') + Word(nums)
number_decimal = Literal('.') + Word(nums)
number = Combine(
	Optional('-') + (number_float | number_integer | number_decimal) + Optional(Suppress(','))
)

# Attribute number without trailing comma (used in width/height="...")
attr_number = Combine(Optional('-') + (number_float | number_integer | number_decimal))

WIDTH = Suppress(Literal('width') + Literal('="')) + attr_number + Suppress(Literal('"'))
HEIGHT = Suppress(Literal('height') + Literal('="')) + attr_number + Suppress(Literal('"'))

MOVE = Caseless('m') + OneOrMore(number[2])
LINE = Caseless('l') + OneOrMore(number[2])
HORIZONTAL = Caseless('h') + number
VERTICAL = Caseless('v') + number
CLOSE = Caseless('z')
CUBIC = Caseless('c') + OneOrMore(number[6])
CUBIC_E = Caseless('s') + OneOrMore(number[4])
QUADRATIC = Caseless('q') + OneOrMore(number[4])
QUADRATIC_E = Caseless('t') + OneOrMore(number[2])
ARC = Caseless('a') + OneOrMore(number[3] + (Literal('0') | Literal('1'))[2] + number[2])


SVG = ZeroOrMore(
	Or(
		map(
			Group,
			[
				MOVE,
				LINE,
				HORIZONTAL,
				VERTICAL,
				CLOSE,
				CUBIC,
				CUBIC_E,
				QUADRATIC,
				QUADRATIC_E,
				ARC,
			],
		)
	)
)


def parse(svg_string: str) -> List[Tuple[List[str], int, int]]:
	for tree, start, end in SVG.scan_string(svg_string):
		if len(tree):
			yield tree, start, end


def parse_dimensions(svg_string: str) -> Tuple[bool, float, float]:
	"""Return (width, height) from SVG element attributes, or (None, None) if absent."""

	w = WIDTH.search_string(svg_string)
	h = HEIGHT.search_string(svg_string)

	if None in [w, h]:
		return False, 0, 0

	return True, float(w[0][0]), float(h[0][0])
