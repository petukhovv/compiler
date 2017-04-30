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
