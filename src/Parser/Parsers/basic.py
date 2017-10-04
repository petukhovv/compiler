from src.Lexer.types import *
from src.Parser.AST.common import *
from src.Parser.combinators import *

"""
Language keywords parsing (Reserved combinator with 'RESERVED' tag).
"""
def keyword(kw):
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

"""
Identifiers parsing (Tag combinator with 'ID' tag).
"""
id = Tag(ID)

"""
Parsing enumeration statement.
"""
def enumeration(alternative_args_parser=None):
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
