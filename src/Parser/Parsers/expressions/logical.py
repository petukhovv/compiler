from ...combinators import Lazy
from ...AST.expressions.logical import RelopBexp, NotBexp, AndBexp, OrBexp
from ...AST.expressions.arithmetic import IntAexp


"""
Precedence levels for binary operations.
"""
bexp_precedence_levels = [
    ['&&'],
    ['||', '!!'],
]


def process_relop(parsed):
    """
    Convert boolean expression value to object of AST-class 'RelopBexp'.
    """
    ((left, op), right) = parsed
    return RelopBexp(op, left, right)


def bexp_relop():
    """
    Parsing boolean expression (arithmetic expression + compare operator + arithmetic expression).
    """
    from ..expressions import arithmetic, strings

    relops = ['<', '<=', '>', '>=', '==', '!=']
    return (arithmetic.aexp() | strings.str_exp() | strings.char_exp() | bexp_group()) + \
       arithmetic.any_operator_in_list(relops) + \
        (arithmetic.aexp() | strings.str_exp() | strings.char_exp() | bexp_group()) ^ process_relop


def bexp_boolop():
    """
    Parsing single value expression (arithmetic expression).
    Convert single value to object of AST-class 'RelopBexp' with '!=' operator and '0' right value.
    """
    from ..expressions import arithmetic

    return arithmetic.aexp() | arithmetic.aexp() ^ (lambda parsed: RelopBexp('!=', parsed, IntAexp(0)))


def bexp_not():
    """
    Parsing 'not' expression (convert expression to object of AST-class 'NotBexp').
    """
    from ..common import keyword

    return keyword('!') + Lazy(bexp_term) ^ (lambda parsed: NotBexp(parsed[1]))


def bexp_group():
    """
    Parse the binary expression in parentheses.
    """
    from ..common import keyword
    from ..expressions import arithmetic

    return keyword('(') + (Lazy(arithmetic.aexp) | Lazy(bexp)) + keyword(')') ^ arithmetic.process_group


def bexp_term(allow_single):
    """
    Parse the binary expression.
    Try to first parse as 'not' expression,
    if not possible - as just binary expressions,
    if not possible - as a parentheses group of binary expressions.
    """
    from ..expressions import arithmetic

    if allow_single:
        return bexp_not() | bexp_relop() | bexp_boolop() | arithmetic.aexp() | bexp_group()
    else:
        return bexp_not() | bexp_relop() | arithmetic.aexp() | bexp_group()


def process_logic(op):
    """
    Parse the binary operation binary expression.
    Convert operator to fabric of AST-classes 'AndBexp' / 'OrBexp'.
    """
    if op == '&&':
        return lambda l, r: AndBexp(l, r)
    elif op == '||' or op == '!!':
        return lambda l, r: OrBexp(l, r)
    else:
        raise RuntimeError('unknown logic operator: ' + op)


def bexp(allow_single=False):
    """
    Main binary expressions parser.
    """
    from ..expressions import arithmetic

    return arithmetic.precedence(bexp_term(allow_single), bexp_precedence_levels, process_logic)
