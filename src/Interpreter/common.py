def pointer(env, element):
    return element.interpret(env)


def enumeration(elements):
    """
    'Enumeration' statement class for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    return elements
