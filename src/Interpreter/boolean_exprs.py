"""
Relation operation boolean expression def for AST.
eval - runtime function for Evaluator (return result of applying the boolean operation to left and right values).
Example: x > 56
"""
def relop_bexp(env, op, left, right):
    left_value = left.eval(env)
    right_value = right.eval(env)
    if op == '<':
        value = left_value < right_value
    elif op == '<=':
        value = left_value <= right_value
    elif op == '>':
        value = left_value > right_value
    elif op == '>=':
        value = left_value >= right_value
    elif op == '==':
        value = left_value == right_value
    elif op == '!=':
        value = left_value != right_value
    else:
        raise RuntimeError('unknown operator: ' + op)
    return value

"""
'And' operation boolean expression def for AST.
eval - runtime function for Evaluator (return result of applying the 'and' operation to left and right values).
Example: x > 56 and x < 61
"""
def and_bexp(env, left, right):
    left_value = left.eval(env)
    right_value = right.eval(env)
    return left_value and right_value

"""
'Or' operation boolean expression def for AST.
eval - runtime function for Evaluator (return result of applying the 'or' operation to left and right values).
Example: x < 11 or x > 100
"""
def or_bexp(env, left, right):
    left_value = left.eval(env)
    right_value = right.eval(env)
    return left_value or right_value

"""
'Not' operation boolean expression def for AST.
eval - runtime function for Evaluator (return result of applying the 'not' operation to value).
Example: x not 11
"""
def not_bexp(env, exp):
    value = exp.eval(env)
    return not value
