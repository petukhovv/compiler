from src.Parser.Language.AST.boolean_exprs import *
from src.Parser.Language.Parsers.arithmetic_exprs import aexp, any_operator_in_list

from src.Parser.Language.Parsers.basic import *

"""
Convert boolean expression value to object of AST-class 'RelopBexp'.
"""
def process_relop(parsed):
    ((left, op), right) = parsed
    return RelopBexp(op, left, right)

"""
Parsing boolean expression (arithmetic expression + compare operator + arithmetic expression).
"""
def bexp_relop():
    relops = ['<', '<=', '>', '>=', '=', '!=']
    return aexp() + any_operator_in_list(relops) + aexp() ^ process_relop

"""
Parsing 'not' expression (convert expression to object of AST-class 'NotBexp').
"""
def bexp_not():
    return keyword('not') + Lazy(bexp_term) ^ (lambda parsed: NotBexp(parsed[1]))