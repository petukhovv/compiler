from equality import *

class Aexp(Equality):
    pass

"""
Integer arithmetic expression class for AST.
eval - runtime function for Evaluator (just return i).
Example: 54
"""
class IntAexp(Aexp):
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return 'IntAexp(%d)' % self.i

    def eval(self, env):
        return self.i

"""
Variable arithmetic expression class for AST.
Example: x
"""
class VarAexp(Aexp):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'VarAexp(%s)' % self.name

"""
Binary operation arithmetic expression class for AST.
Example: x + 54
"""
class BinopAexp(Aexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return 'BinopAexp(%s, %s, %s)' % (self.op, self.left, self.right)
