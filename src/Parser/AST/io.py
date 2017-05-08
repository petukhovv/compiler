import sys

from equality import *

"""
Base class for statement classes.
"""
class IO(Equality):
    pass

"""
'Read' statement class for AST.
eval - runtime function for Evaluator (get value from stdin).
"""
class ReadStatement(IO):
    def __repr__(self):
        return 'ReadStatement'

    def eval(self, env):
        value = sys.stdin.readline()
        try:
            return int(value)
        except ValueError:
            raise RuntimeError(value + ' is not integer')

"""
'Write' statement class for AST.
eval - runtime function for Evaluator (write value to stdout).
"""
class WriteStatement(IO):
    def __init__(self, aexp):
        self.aexp = aexp

    def __repr__(self):
        return 'WriteStatement(%s)' % self.aexp

    def eval(self, env):
        value = self.aexp.eval(env)
        if type(value) is bool:
            value = int(value)
        sys.stdout.write(str(value) + '\n')
