def if_statement(env, node):
    """
    'If' statement def for AST.
    interpret - runtime function for Evaluator (true of false statement depending on condition).
    """
    condition_value = node.condition.interpret(env)
    if condition_value:
        node.true_stmt.interpret(env)
    else:
        if node.alternatives_stmt:
            for alternative_stmt in node.alternatives_stmt:
                alternative_condition_value = alternative_stmt.interpret(env)
                if alternative_condition_value:
                    return True
        if node.false_stmt:
            node.false_stmt.interpret(env)
    return condition_value
