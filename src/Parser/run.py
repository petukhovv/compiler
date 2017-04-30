from src.Parser.Parsers.statements import stmt_list
from src.Parser.combinators import *

"""
Run the parser with the input tokens from the 0-position.
"""
def parse(tokens):
    ast = parser()(tokens, 0)
    return ast

"""
Run the top-level parser (statement list).
"""
def parser():
    return Phrase(stmt_list())
