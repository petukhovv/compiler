def pointer(env, node):
    return node.element.interpret(node.env)


def enumeration(env, node):
    """
    'Enumeration' statement class for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    return node.elements
