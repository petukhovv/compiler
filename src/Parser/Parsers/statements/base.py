from functools import reduce

from ...combinators import Rep, Exp
from ...AST.common import CompoundStatement


def stmt():
    """
    Main statement parser.
    Try to first parse as 'assign' statement,
    if not possible - as 'if' statement,
    if not possible - as 'while' statement.
    """
    from ..expressions.arithmetic import aexp
    from ..expressions.objects import object_method
    from ..statements.conditional import if_stmt
    from ..statements.assignment import assign_stmt
    from ..statements.loop import while_stmt, repeat_stmt, for_stmt
    from ..statements.return_ import return_stmt
    from ..statements.skip import skip_stmt
    from ..expressions.call import fun_call_stmt
    from ..statements.write import write_stmt

    return assign_stmt() | \
        if_stmt() | \
        while_stmt() | \
        repeat_stmt() | \
        for_stmt() | \
        return_stmt() | \
        write_stmt() | \
        fun_call_stmt() | \
        object_method() | \
        skip_stmt() | \
        aexp()


def stmt_list():
    """
    Parsing statement list (by ';' separator).
    Example:
    x := 56;
    y := 12;
    z := 512
    """
    from ..common import keyword
    from ..declarations.function import fun

    def process_stmt(x):
        return lambda l, r: CompoundStatement(l, r)

    def process(parsed_list):
        if len(parsed_list) == 1:
            return parsed_list[0]
        return reduce(lambda stmt1, stmt2: CompoundStatement(stmt1, stmt2), parsed_list)
    return Rep(fun() | Exp(stmt(), keyword(';') ^ process_stmt)) ^ process
