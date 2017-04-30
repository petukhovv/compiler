from src.Parser.Language.AST.arithmetic_exprs import *

from src.Parser.Language.Parsers.basic import *

"""
Converts the values returned by 'num' and 'id' to the object of AST classes.
"""
def aexp_value():
    return (num ^ (lambda i: IntAexp(i))) | \
           (id ^ (lambda v: VarAexp(v)))
