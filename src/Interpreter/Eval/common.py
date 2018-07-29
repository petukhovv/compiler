def compound_statement(env, node):
    """
    Compound statement def for AST.
    interpret - runtime function for Evaluator (interpret first and second statement operators).
    """
    node.first.interpret(env)
    node.second.interpret(env)


def pointer(env, node):
    return node.element.interpret(node.env)


def enumeration(env, node):
    """
    'Enumeration' statement class for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    return node.elements
