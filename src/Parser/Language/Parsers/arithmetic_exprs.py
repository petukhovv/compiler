from src.Parser.Language.AST.arithmetic_exprs import *

from src.Parser.Language.Parsers.basic import *

"""

"""
def any_operator_in_list(ops):
    op_parsers = [keyword(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser

"""
Precedence levels for arithmetic operations.
"""
aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]

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

"""
Parse the arithmetic expression.
Try to first parse as just arithmetic expressions, if not possible - as a parentheses group.
"""
def aexp_term():
    return aexp_value() | aexp_group()

"""
Parse the binary operation arithmetic expression.
Convert operator to fabric of binary operations.
"""
def process_binop(operator):
    return lambda l, r: BinopAexp(operator, l, r)
