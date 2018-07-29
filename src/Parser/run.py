from .combinators import Phrase


def parse(tokens):
    """
    Run the parser with the input tokens from the 0-position.
    """
    ast = parser()(tokens, 0)
    return ast


def parser():
    """
    Run the top-level parser (statement list).
    """
    from .Parsers.statements import base

    return Phrase(base.stmt_list())
