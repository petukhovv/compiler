from src.Parser.Language.AST.statements import *
from src.Parser.Language.Parsers.arithmetic_exprs import aexp

from src.Parser.Language.Parsers.basic import *

"""
Parsing simple assign statement.
Example: x := 56
"""
def assign_stmt():
    def process(parsed):
        ((name, _), exp) = parsed
        return AssignStatement(name, exp)
    return id + keyword(':=') + aexp() ^ process

"""
Parsing statement list (by ';' separator).
Example:
x := 56;
y := 12;
z := 512
"""
def stmt_list():
    separator = keyword(';') ^ (lambda x: lambda l, r: CompoundStatement(l, r))
    return Exp(stmt(), separator)
