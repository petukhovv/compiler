import sys

from src.Parser.Parsers.basic import *
from src.Parser.Parsers.arithmetic_exprs import aexp
from src.Parser.Parsers.boolean_exprs import bexp

from src.Parser.AST.functions import *

statements = sys.modules[__package__ + '.statements']

"""
Parsing function arguments statement.
"""
def args(alternative_args_parser=None):
    def process(parsed_list):
        variables = []
        for parsed in parsed_list:
            (variable, _) = parsed
            variables.append(variable)
        return Arguments(variables)
    if alternative_args_parser:
        args_parser = alternative_args_parser
    else:
        args_parser = id
    return Rep(args_parser + Opt(keyword(','))) ^ process

"""
Parsing function arguments statement (call point).
"""
def args_call():
    return args(alternative_args_parser=(aexp() | bexp()))

"""
Parsing function statement.
"""
def fun():
    def process(parsed):
        (((((((_, name), _), args), _), _), body), _) = parsed
        return Function(name, args, body)
    return keyword('fun') + id + \
        keyword('(') + Opt(args()) + keyword(')') + \
        keyword('begin') + Opt(Lazy(statements.stmt_list)) + \
        keyword('end') ^ process

"""
Parsing function call statement.
"""
def return_stmt():
    def process(parsed):
        (_, expr) = parsed
        return ReturnStatement(expr)
    return keyword('return') + Opt(aexp() | bexp()) ^ process

"""
Parsing function call statement.
"""
def fun_call_stmt():
    def process(parsed):
        (((name, _), args), _) = parsed
        return FunctionCallStatement(name, args)
    return id + \
        keyword('(') + Opt(Lazy(args_call)) + keyword(')') ^ process
