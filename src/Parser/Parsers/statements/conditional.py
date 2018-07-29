from ...combinators import Lazy, Opt, Rep
from ...AST.statements.conditional import IfStatement


def if_stmt():
    """
    Parsing 'if' statement.
    """
    from ..common import keyword
    from ..expressions import logical
    from ..statements import base

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
    return keyword('if') + logical.bexp(allow_single=True) + keyword('then') + Lazy(base.stmt_list) + \
           Opt(Rep(keyword('elif') + logical.bexp(allow_single=True) + keyword('then') + Lazy(base.stmt_list))) + \
           Opt(keyword('else') + Lazy(base.stmt_list)) + \
           keyword('fi') ^ process

