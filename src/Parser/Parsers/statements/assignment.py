from ...AST.statements.assignment import AssignmentStatement
from ...AST.expressions.arithmetic import VarAexp


def assign_stmt():
    """
    Parsing simple assign statement.
    Example: x := 56
    """
    from ..common import id, keyword
    from ..expressions import arrays, arithmetic, objects, logical, read, strings
    from ..declarations import object

    def process(parsed):
        ((name, _), exp) = parsed
        return AssignmentStatement(name, exp)
    return (arrays.el_exp() | objects.object_val() | id ^ (lambda v: VarAexp(v))) + keyword(':=') + \
        (logical.bexp(allow_single=True) | arithmetic.aexp() | objects.object_method() | objects.object_val() | logical.bexp() | read.read_stmt()
         | strings.str_exp() | strings.char_exp() | arrays.arr_exp() | object.object_def()) ^ process
