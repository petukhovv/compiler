import sys


def read_statement(env, node):
    """
    'Read' statement def for AST.
    interpret - runtime function for Evaluator (get value from stdin).
    """
    value = sys.stdin.readline()
    sys.stdout.write('> ')
    try:
        return int(value)
    except ValueError:
        raise RuntimeError(value + ' is not integer')


def write_statement(env, node):
    """
    'Write' statement def for AST.
    interpret - runtime function for Evaluator (write value to stdout).
    """
    value = node.aexp.interpret(env)
    if type(value) is bool:
        value = int(value)
    sys.stdout.write(str(value) + '\n')
