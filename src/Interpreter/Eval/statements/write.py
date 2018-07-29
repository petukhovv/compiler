import sys


def write_statement(env, node):
    """
    'Write' statement def for AST.
    interpret - runtime function for Evaluator (write value to stdout).
    """
    value = node.aexp.interpret(env)
    if type(value) is bool:
        value = int(value)
    sys.stdout.write(str(value) + '\n')
