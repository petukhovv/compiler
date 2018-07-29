from ...combinators import Lazy
from ...AST.statements.loop import WhileStatement, ForStatement, RepeatStatement


def while_stmt():
    """
    Parsing 'while' statement.
    """
    from ..common import keyword
    from ..expressions.logical import bexp
    from .base import stmt_list

    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return WhileStatement(condition, body)
    return keyword('while') + bexp(allow_single=True) + \
        keyword('do') + Lazy(stmt_list) + \
        keyword('od') ^ process


def for_stmt():
    """
    Parsing 'for' statement.
    """
    from ..common import keyword
    from ..expressions.logical import bexp
    from .base import stmt_list
    from .assignment import assign_stmt
    from .skip import skip_stmt

    def process(parsed):
        ((((((((_, stmt1), _), stmt2), _), stmt3), _), body), _) = parsed
        return ForStatement(stmt1, stmt2, stmt3, body)
    return keyword('for') + (assign_stmt() | skip_stmt()) + keyword(',') + \
        bexp(allow_single=True) + keyword(',') + \
        assign_stmt() + keyword('do') + \
        Lazy(stmt_list) + keyword('od') ^ process


def repeat_stmt():
    """
    Parsing 'repeat' statement.
    """
    from ..common import keyword
    from ..expressions.logical import bexp
    from .base import stmt_list

    def process(parsed):
        (((_, body), _), condition) = parsed
        return RepeatStatement(condition, body)
    return keyword('repeat') + Lazy(stmt_list) + \
        keyword('until') + bexp(allow_single=True) ^ process
