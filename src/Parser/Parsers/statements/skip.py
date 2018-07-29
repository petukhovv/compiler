from ...AST.statements.skip import SkipStatement


def skip_stmt():
    """
    Parsing 'skip' statement.
    """
    from ..common import keyword

    return keyword('skip') ^ (lambda parsed: SkipStatement())
