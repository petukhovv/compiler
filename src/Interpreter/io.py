import sys

"""
'Read' statement def for AST.
eval - runtime function for Evaluator (get value from stdin).
"""
def read_statement(env):
    value = sys.stdin.readline()
    sys.stdout.write('> ')
    try:
        return int(value)
    except ValueError:
        raise RuntimeError(value + ' is not integer')

"""
'Write' statement def for AST.
eval - runtime function for Evaluator (write value to stdout).
"""
def write_statement(env, aexp):
    value = aexp.eval(env)
    if type(value) is bool:
        value = int(value)
    sys.stdout.write(str(value) + '\n')
