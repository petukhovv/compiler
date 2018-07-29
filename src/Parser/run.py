from .combinators import Phrase

positions = []


class Position:
    def __init__(self, current):
        self.current = current

    def __eq__(self, other):
        return self.current == other

    def __ne__(self, other):
        return self.current != other

    def __lt__(self, other):
        return self.current < other

    def __gt__(self, other):
        return self.current > other

    def __le__(self, other):
        return self.current <= other

    def __ge__(self, other):
        return self.current >= other

    def __add__(self, other):
        position = Position(self.current + other)
        positions.append(position)

        return position

    def __index__(self):
        return self.current


def parse(tokens):
    """
    Run the parser with the input tokens from the 0-position.
    """
    ast = parser()(tokens, Position(0))

    max_position = 0

    for position in positions:
        if position > max_position:
            max_position = position.current

    if len(tokens) != max_position:
        print("Invalid syntax near: ", end='')
        for i in range(max(max_position - 1, 0), min(max_position + 10, len(tokens))):
            print(tokens[i][0], end=' ')

        print()

    return ast


def parser():
    """
    Run the top-level parser (statement list).
    """
    from .Parsers.statements import base

    return Phrase(base.stmt_list())
