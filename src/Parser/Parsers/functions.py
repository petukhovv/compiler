from ..AST.functions import *

from .boolean_exprs import bexp
from .io import *
from .arrays import *


statements = sys.modules[__package__ + '.statements']

predefined = {
    'strings': string_predefined_functions,
    'io': io_predefined_functions,
    'arrays': array_predefined_functions
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


def args_call():
    """
    Parsing function arguments statement (call point).
    """
    return enumeration(alternative_args_parser=(aexp() | bexp() | str_exp() | char_exp() | arr_exp()))


def fun():
    """
    Parsing function statement.
    """
    def process(parsed):
        (((((((_, name), _), args), _), _), body), _) = parsed
        return Function(name, args, body)
    return keyword('fun') + id + \
        keyword('(') + Opt(enumeration()) + keyword(')') + \
           keyword('begin') + Opt(Lazy(statements.stmt_list)) + \
        keyword('end') ^ process


def return_stmt():
    """
    Parsing function call statement.
    """
    def process(parsed):
        (_, expr) = parsed
        return ReturnStatement(expr)
    return keyword('return') + Opt(aexp() | bexp() | str_exp() | char_exp() | arr_exp()) ^ process


def fun_call_stmt():
    """
    Parsing function call statement.
    """
    def process(parsed):
        (((name, _), args), _) = parsed
        if is_predefined(name):
            return get_predefined(name)(args)
        else:
            return FunctionCallStatement(name, args)
    return id + \
        keyword('(') + Opt(Lazy(args_call)) + keyword(')') ^ process
