from src.Parser.combinators import *

def parse(tokens):
    ast = parser()(tokens, 0)
    return ast

def parser():
    return None
