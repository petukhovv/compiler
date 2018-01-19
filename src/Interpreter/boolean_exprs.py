def relop_bexp(env, op, left, right):
    """
    Relation operation boolean expression def for AST.
    eval - runtime function for Evaluator (return result of applying the boolean operation to left and right values).
    Example: x > 56
    """
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


def and_bexp(env, left, right):
    """
    'And' operation boolean expression def for AST.
    eval - runtime function for Evaluator (return result of applying the 'and' operation to left and right values).
    Example: x > 56 and x < 61
    """
    left_value = left.eval(env)
    right_value = right.eval(env)
    return 1 if left_value and right_value else 0


def or_bexp(env, left, right):
    """
    'Or' operation boolean expression def for AST.
    eval - runtime function for Evaluator (return result of applying the 'or' operation to left and right values).
    Example: x < 11 or x > 100
    """
    left_value = left.eval(env)
    right_value = right.eval(env)
    return 1 if left_value or right_value else 0


def not_bexp(env, exp):
    """
    'Not' operation boolean expression def for AST.
    eval - runtime function for Evaluator (return result of applying the 'not' operation to value).
    Example: x not 11
    """
    value = exp.eval(env)
    return 1 if not value else 0
