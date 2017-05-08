from src.Parser.Parsers.basic import *

from src.Parser.AST.strings import *

"""
Main arithmetic expressions parser.
"""
def str_exp():
    return Tag(STRING) ^ String
