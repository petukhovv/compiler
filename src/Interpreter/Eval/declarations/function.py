def function(env, node):
    """
    'Function' statement def for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    env['f'][node.name] = {
        'args': node.args,
        'body': node.body
    }
