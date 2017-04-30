from src.Parser.Language.AST.arithmetic_exprs import *

from src.Parser.Language.Parsers.basic import *

"""
Converts the values returned by 'num' and 'id' to the object of AST classes.
First of all, try to parse integer, if unsuccessful, try to parse as a variable (via Alternate combinator).
"""
def aexp_value():
    return (num ^ (lambda i: IntAexp(i))) | \
           (id ^ (lambda v: VarAexp(v)))

"""
Removes parentheses and returns an expression in them.
"""
def process_group(parsed):
    ((_, p), _) = parsed
    return p

"""
Parse the arithmetic expression in parentheses.
"""
def aexp_group():
    return keyword('(') + Lazy(aexp) + keyword(')') ^ process_group
