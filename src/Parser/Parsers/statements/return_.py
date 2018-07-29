from ...combinators import Opt
from ...AST.statements.return_ import ReturnStatement


def return_stmt():
    """
    Parsing function call statement.
    """
    from ..common import keyword
    from ..declarations.object import object_def
    from ..expressions.objects import object_val
    from ..expressions.arithmetic import aexp
    from ..expressions.logical import bexp
    from ..expressions.strings import str_exp, char_exp
    from ..expressions.arrays import arr_exp

    def process(parsed):
        (_, expr) = parsed
        return ReturnStatement(expr)
    return keyword('return') + Opt(object_def() | object_val() | aexp() | bexp() | str_exp() | char_exp() | arr_exp()) ^ process

