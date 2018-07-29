from ...combinators import Opt
from ...AST.statements.return_ import ReturnStatement


def return_stmt():
    """
    Parsing function call statement.
    """
    from ..common import keyword
    from ..declarations import object
    from ..expressions import objects, arithmetic, logical, strings, arrays

    def process(parsed):
        (_, expr) = parsed
        return ReturnStatement(expr)
    return keyword('return') + Opt(object.object_def() | objects.object_val() | arithmetic.aexp() | logical.bexp() | strings.str_exp() | strings.char_exp() | arrays.arr_exp()) ^ process

