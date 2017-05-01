from src.Parser.Parsers.basic import *

from src.Parser.AST.arithmetic_exprs import *

"""
Returns the parser appropriate to the keyword list (ops).
"""
def any_operator_in_list(ops):
    op_parsers = [keyword(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser

"""
Precedence levels for arithmetic operations.
"""
aexp_precedence_levels = [
    ['*', '/', '%'],
    ['+', '-'],
]

"""
Prioritizes operations (brackets) according to the precedence levels.
Example:
    Input: 4 * a + b / 2 - (6 + c)
    1) E0(4) * E0(a) + E0(b) / E0(2) - E0(6+c)
    2) E1(4*a) + E1(b/2) - E1(6+c)
    3) E2((4*a)+(b/2)-(6+c))
"""
def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine
    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser

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
Try to first parse as just arithmetic expressions,
if not possible - as a parentheses group of arithmetic expressions.
"""
def aexp_term():
    return aexp_value() | aexp_group()

"""
Parse the binary operation arithmetic expression.
Convert operator to fabric of AST-classes 'BinopAexp'.
"""
def process_binop(operator):
    return lambda l, r: BinopAexp(operator, l, r)

"""
Main arithmetic expressions parser.
"""
def aexp():
    return precedence(aexp_term(),
                      aexp_precedence_levels,
                      process_binop)
