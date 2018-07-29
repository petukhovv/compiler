from ...AST.statements.assignment import AssignmentStatement
from ...AST.expressions.arithmetic import VarAexp


def assign_stmt():
    """
    Parsing simple assign statement.
    Example: x := 56
    """
    from ..common import id, keyword
    from ..expressions.arrays import el_exp, arr_exp
    from ..expressions.arithmetic import aexp
    from ..expressions.objects import object_method, object_val
    from ..expressions.logical import bexp
    from ..expressions.read import read_stmt
    from ..expressions.strings import str_exp, char_exp
    from ..declarations.object import object_def

    def process(parsed):
        ((name, _), exp) = parsed
        return AssignmentStatement(name, exp)
    return (el_exp() | object_val() | id ^ (lambda v: VarAexp(v))) + keyword(':=') + \
        (bexp(allow_single=True) | aexp() | object_method() | object_val() | bexp() | read_stmt()
         | str_exp() | char_exp() | arr_exp() | object_def()) ^ process
