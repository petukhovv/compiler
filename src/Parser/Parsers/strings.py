from src.Parser.Parsers.basic import *

from src.Parser.AST.strings import *

string_predefined_functions = {
    'strlen': StrLen,
    'strget': StrGet
    # TODO: add 'strsub', 'strdup', 'strset', 'strcat', 'strcmp' and 'strmake'
}

"""
Main arithmetic expressions parser.
"""
def str_exp():
    return Tag(STRING) ^ String
