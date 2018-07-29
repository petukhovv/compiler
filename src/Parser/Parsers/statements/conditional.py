from ...combinators import Lazy, Opt, Rep
from ...AST.statements.conditional import IfStatement


def if_stmt():
    """
    Parsing 'if' statement.
    """
    from ..common import keyword
    from ..expressions.logical import bexp
    from .base import stmt_list

    def process(parsed):
        ((((((_, condition), _), true_stmt), alternatives_stmt_parsed), false_stmt_parsed), _) = parsed
        if false_stmt_parsed:
            (_, false_stmt) = false_stmt_parsed
        else:
            false_stmt = None
        if alternatives_stmt_parsed:
            alternatives_stmt = []
            for alternative_stmt_parsed in alternatives_stmt_parsed:
                (((_, alternative_condition), _), alternative_body) = alternative_stmt_parsed
                alternatives_stmt.append(IfStatement(alternative_condition, alternative_body, None))
        else:
            alternatives_stmt = None
        return IfStatement(condition, true_stmt, alternatives_stmt, false_stmt)
    return keyword('if') + bexp(allow_single=True) + keyword('then') + Lazy(stmt_list) + \
           Opt(Rep(keyword('elif') + bexp(allow_single=True) + keyword('then') + Lazy(stmt_list))) + \
           Opt(keyword('else') + Lazy(stmt_list)) + \
           keyword('fi') ^ process

