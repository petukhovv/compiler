import sys

"""
'Read' statement class for AST.
eval - runtime function for Evaluator (get value from stdin).
"""
class ReadStatement:
    def __repr__(self):
        return 'ReadStatement'

    def eval(self, env):
        value = sys.stdin.readline()
        sys.stdout.write('> ')
        try:
            return int(value)
        except ValueError:
            raise RuntimeError(value + ' is not integer')

"""
'Write' statement class for AST.
eval - runtime function for Evaluator (write value to stdout).
"""
class WriteStatement:
    def __init__(self, aexp):
        self.aexp = aexp

    def eval(self, env):
        value = self.aexp.eval(env)
        if type(value) is bool:
            value = int(value)
        sys.stdout.write(str(value) + '\n')
