from src.Parser.Language.AST.boolean_exprs import *
from src.Parser.Language.Parsers.arithmetic_exprs import aexp, any_operator_in_list

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
