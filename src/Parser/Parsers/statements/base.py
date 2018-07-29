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
    from ..expressions import arithmetic, objects, call
    from ..statements import conditional, assignment, loop, return_, skip, write

    return assignment.assign_stmt() | \
        conditional.if_stmt() | \
        loop.while_stmt() | \
        loop.repeat_stmt() | \
        loop.for_stmt() | \
        return_.return_stmt() | \
        write.write_stmt() | \
        call.fun_call_stmt() | \
        objects.object_method() | \
        skip.skip_stmt() | \
        arithmetic.aexp()


def stmt_list():
    """
    Parsing statement list (by ';' separator).
    Example:
    x := 56;
    y := 12;
    z := 512
    """
    from ..common import keyword
    from ..declarations import function

    def process_stmt(x):
        return lambda l, r: CompoundStatement(l, r)

    def process(parsed_list):
        if len(parsed_list) == 1:
            return parsed_list[0]
        return reduce(lambda stmt1, stmt2: CompoundStatement(stmt1, stmt2), parsed_list)
    return Rep(function.fun() | Exp(stmt(), keyword(';') ^ process_stmt)) ^ process
