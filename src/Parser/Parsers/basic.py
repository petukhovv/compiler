from Lexer.types import *

from ..AST.common import *
from ..combinators import *


def keyword(kw):
    """
    Language keywords parsing (Reserved combinator with 'RESERVED' tag).
    """
    return Reserved(kw, RESERVED)


"""
Integers parsing (Tag combinator with 'INT' tag).
A Process combinator (^ operator) is also used to convert token into an integer.
"""
num = Tag(INT) ^ (lambda i: int(i))


def boolean_parser(flag):
    if flag == 'true':
        return 1
    elif flag == 'false':
        return 0


boolean = Tag(BOOLEAN) ^ boolean_parser

""" Identifiers parsing (Tag combinator with 'ID' tag). """
id = Tag(ID)


def enumeration(alternative_args_parser=None):
    """ Parsing enumeration statement. """
    def process(parsed_list):
        variables = []
        for parsed in parsed_list:
            (variable, _) = parsed
            variables.append(variable)
        return Enumeration(variables)
    if alternative_args_parser:
        args_parser = alternative_args_parser
    else:
        args_parser = id
    return Rep(args_parser + Opt(keyword(','))) ^ process
