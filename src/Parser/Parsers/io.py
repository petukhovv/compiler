from ..AST.io import *

from .arithmetic_exprs import *

io_predefined_functions = {
    'read': ReadStatement,
    'write': WriteStatement
}


def read_stmt():
    """ Parsing 'read' statement. """
    return keyword('read') + keyword('(') + keyword(')') ^ (lambda parsed: ReadStatement())


def write_stmt():
    """ Parsing 'write' statement. """
    def process(parsed):
        (((_, _), name), _) = parsed
        return WriteStatement(name)
    return keyword('write') + \
        keyword('(') + aexp() + keyword(')') ^ process
