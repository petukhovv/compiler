from src.Parser.Parsers.arithmetic_exprs import *

from src.Parser.AST.io import *

"""
Parsing 'read' statement.
"""
def read_stmt():
    return keyword('read') + keyword('(') + keyword(')') ^ (lambda parsed: ReadStatement())

"""
Parsing 'write' statement.
"""
def write_stmt():
    def process(parsed):
        (((_, _), name), _) = parsed
        return WriteStatement(name)
    return keyword('write') + \
        keyword('(') + aexp() + keyword(')') ^ process
