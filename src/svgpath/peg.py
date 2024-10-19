from typing import Tuple, List
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
number_float = Word(nums) + Literal(".") + Word(nums)
number_decimal = Literal(".") + Word(nums)
number = Combine(
    Optional("-")
    + (number_float | number_integer | number_decimal)
    + Optional(Suppress(","))
)

MOVE = Caseless("m") + number[2]
LINE = Caseless("l") + OneOrMore(number[2])
HORIZONTAL = Caseless("h") + number
VERTICAL = Caseless("v") + number
CLOSE = Caseless("z")
CUBIC = Caseless("c") + OneOrMore(number[6])
CUBIC_E = Caseless("s") + OneOrMore(number[4])
QUADRATIC = Caseless("q") + OneOrMore(number[4])
QUADRATIC_E = Caseless("t") + OneOrMore(number[2])
ARC = Caseless("a") + OneOrMore(
    number[3] + (Literal("0") | Literal("1"))[2] + number[2]
)


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
