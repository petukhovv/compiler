def return_statement(env, node):
    """
    'Return' statement def for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    env['r'] = node.expr.interpret(env)
    return
