from ...Helpers.environment import Environment


def while_statement(env, node):
    """
    'While' statement def for AST.
    interpret - runtime function for Evaluator (body interpret while condition).
    """
    while node.condition.interpret(env):
        node.body.interpret(env)


def for_statement(env, node):
    """
    'For' statement def for AST.
    interpret - runtime function for Evaluator ('for' loop).
    """
    node.stmt1.interpret(env)
    while node.stmt2.interpret(env):
        iteration_env = Environment(env).create()
        node.body.interpret(iteration_env)
        node.stmt3.interpret(env)
    return


def repeat_statement(env, node):
    """
    'Repeat' statement def for AST.
    interpret - runtime function for Evaluator (body interpret while condition).
    """
    while True:
        node.body.interpret(env)
        condition_value = node.condition.interpret(env)
        if condition_value:
            break
