from src.Parser.Parsers.boolean_exprs import bexp
from src.Parser.Parsers.strings import *
from src.Parser.Parsers.io import *

from src.Parser.AST.functions import *

statements = sys.modules[__package__ + '.statements']

predefined = {
    'strings': string_predefined_functions,
    'io': io_predefined_functions
}

def is_predefined(name):
    for entity in predefined:
        if name in predefined[entity].keys():
            return True
    return False

def get_predefined(name):
    for entity in predefined:
        if name in predefined[entity].keys():
            return predefined[entity][name]
    return None

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
    return args(alternative_args_parser=(aexp() | bexp() | str_exp() | char_exp()))

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
        if is_predefined(name):
            return get_predefined(name)(args)
        else:
            return FunctionCallStatement(name, args)
    return id + \
        keyword('(') + Opt(Lazy(args_call)) + keyword(')') ^ process
