def relop_bexp(env, node):
    """
    Relation operation boolean expression def for AST.
    interpret - runtime function for Evaluator (return result of applying the boolean operation to left and right values).
    Example: x > 56
    """
    left_value = node.left.interpret(env)
    right_value = node.right.interpret(env)
    if node.op == '<':
        value = left_value < right_value
    elif node.op == '<=':
        value = left_value <= right_value
    elif node.op == '>':
        value = left_value > right_value
    elif node.op == '>=':
        value = left_value >= right_value
    elif node.op == '==':
        value = left_value == right_value
    elif node.op == '!=':
        value = left_value != right_value
    else:
        raise RuntimeError('unknown operator: ' + node.op)
    return value


def and_bexp(env, node):
    """
    'And' operation boolean expression def for AST.
    interpret - runtime function for Evaluator (return result of applying the 'and' operation to left and right values).
    Example: x > 56 and x < 61
    """
    left_value = node.left.interpret(env)
    right_value = node.right.interpret(env)
    return 1 if left_value and right_value else 0


def or_bexp(env, ndoe):
    """
    'Or' operation boolean expression def for AST.
    interpret - runtime function for Evaluator (return result of applying the 'or' operation to left and right values).
    Example: x < 11 or x > 100
    """
    left_value = node.left.interpret(env)
    right_value = node.right.interpret(env)
    return 1 if left_value or right_value else 0


def not_bexp(env, node):
    """
    'Not' operation boolean expression def for AST.
    interpret - runtime function for Evaluator (return result of applying the 'not' operation to value).
    Example: x not 11
    """
    value = node.exp.interpret(env)
    return 1 if not value else 0
