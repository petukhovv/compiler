from ...combinators import Lazy
from ...AST.statements.loop import WhileStatement, ForStatement, RepeatStatement


def while_stmt():
    """
    Parsing 'while' statement.
    """
    from ..common import keyword
    from ..expressions import logical
    from ..statements import base

    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return WhileStatement(condition, body)
    return keyword('while') + logical.bexp(allow_single=True) + \
        keyword('do') + Lazy(base.stmt_list) + \
        keyword('od') ^ process


def for_stmt():
    """
    Parsing 'for' statement.
    """
    from ..common import keyword
    from ..expressions import logical
    from ..statements import base, assignment, skip

    def process(parsed):
        ((((((((_, stmt1), _), stmt2), _), stmt3), _), body), _) = parsed
        return ForStatement(stmt1, stmt2, stmt3, body)
    return keyword('for') + (assignment.assign_stmt() | skip.skip_stmt()) + keyword(',') + \
        logical.bexp(allow_single=True) + keyword(',') + \
        assignment.assign_stmt() + keyword('do') + \
        Lazy(base.stmt_list) + keyword('od') ^ process


def repeat_stmt():
    """
    Parsing 'repeat' statement.
    """
    from ..common import keyword
    from ..expressions import logical
    from ..statements import base

    def process(parsed):
        (((_, body), _), condition) = parsed
        return RepeatStatement(condition, body)
    return keyword('repeat') + Lazy(base.stmt_list) + \
        keyword('until') + logical.bexp(allow_single=True) ^ process
