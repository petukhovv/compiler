from ...combinators import Opt, Lazy
from ...AST.expressions.call import FunctionCallStatement
from ...AST.expressions.read import ReadStatement
from ...AST.statements.write import WriteStatement

from ..statements.strings import string_predefined_functions as string_statements_predefined_functions
from .strings import string_predefined_functions as string_expressions_predefined_functions
from .arrays import array_predefined_functions


predefined = {
    'strings': {**string_expressions_predefined_functions, **string_statements_predefined_functions},
    'io': {
        'read': ReadStatement,
        'write': WriteStatement
    },
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


def fun_call_stmt():
    """
    Parsing function call statement.
    """
    from ..common import keyword, id
    from ..expressions import arguments

    def process(parsed):
        (((name, _), args), _) = parsed
        if is_predefined(name):
            return get_predefined(name)(args)
        else:
            return FunctionCallStatement(name, args)
    return id + \
        keyword('(') + Opt(Lazy(arguments.arguments)) + keyword(')') ^ process