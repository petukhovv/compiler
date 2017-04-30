from equality import *

class Aexp(Equality):
    pass

"""
Integer arithmetic expression class for AST.
eval - runtime function for Evaluator (just return i).
"""
class IntAexp(Aexp):
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return 'IntAexp(%d)' % self.i

    def eval(self, env):
        return self.i

