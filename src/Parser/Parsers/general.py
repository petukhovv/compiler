from src.Parser.Parsers import stmt_list
from src.Parser.combinators import *


def parse(tokens):
    ast = parser()(tokens, 0)
    return ast

def parser():
    return Phrase(stmt_list())
