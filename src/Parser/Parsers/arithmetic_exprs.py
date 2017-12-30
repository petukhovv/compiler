from functools import reduce

from .arrays import *

statements = sys.modules[__package__ + '.statements']


def any_operator_in_list(ops):
    """
    Returns the parser appropriate to the keyword list (ops).
    """
    op_parsers = [keyword(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser


""" Precedence levels for arithmetic operations. """
aexp_precedence_levels = [
    ['*', '/', '%'],
    ['+', '-'],
]


def precedence(value_parser, precedence_levels, combine):
    """
    Prioritizes operations (brackets) according to the precedence levels.
    Example:
        Input: 4 * a + b / 2 - (6 + c)
        1) E0(4) * E0(a) + E0(b) / E0(2) - E0(6+c)
        2) E1(4*a) + E1(b/2) - E1(6+c)
        3) E2((4*a)+(b/2)-(6+c))
    """
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine
    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser


def aexp_value():
    """
    Converts the values returned by 'num' and 'id' to the object of AST classes.
    First of all, try to parse integer, if unsuccessful, try to parse as a variable (via Alternate combinator).
    """
    return el_exp() | statements.fun_call_stmt() | \
        ((boolean | num) ^ (lambda i: IntAexp(i))) | \
        (id ^ (lambda v: VarAexp(v)))


def process_group(parsed):
    """
    Removes parentheses and returns an expression in them.
    """
    ((_, p), _) = parsed
    return p


def aexp_group():
    """
    Parse the arithmetic expression in parentheses.
    """
    return keyword('(') + Lazy(aexp) + keyword(')') ^ process_group


def aexp_term():
    """
    Parse the arithmetic expression.
    Try to first parse as just arithmetic expressions,
    if not possible - as a parentheses group of arithmetic expressions.
    """
    return aexp_value() | aexp_group()


def process_binop(operator):
    """
    Parse the binary operation arithmetic expression.
    Convert operator to fabric of AST-classes 'BinopAexp'.
    """
    return lambda l, r: BinopAexp(operator, l, r)


def aexp():
    """
    Main arithmetic expressions parser.
    """
    return precedence(aexp_term(),
                      aexp_precedence_levels,
                      process_binop)
