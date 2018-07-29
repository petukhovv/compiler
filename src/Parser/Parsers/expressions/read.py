from ...AST.expressions.read import ReadStatement


def read_stmt():
    """ Parsing 'read' statement. """
    from ..common import keyword

    return keyword('read') + keyword('(') + keyword(')') ^ (lambda parsed: ReadStatement())
