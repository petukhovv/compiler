from equality import *

"""
Base class for arithmetic expression classes.
"""
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
eval - runtime function for Evaluator (return variable from environment by name).
Example: x
"""
class VarAexp(Aexp):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'VarAexp(%s)' % self.name

    def eval(self, env):
        if self.name in env:
            return env[self.name]
        else:
            return 0

"""
Binary operation arithmetic expression class for AST.
eval - runtime function for Evaluator (return result of applying the aoperation to left and right values).
Example: x + 54
"""
class BinopAexp(Aexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return 'BinopAexp(%s, %s, %s)' % (self.op, self.left, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '+':
            value = left_value + right_value
        elif self.op == '-':
            value = left_value - right_value
        elif self.op == '*':
            value = left_value * right_value
        elif self.op == '/':
            value = left_value / right_value
        elif self.op == '%':
            value = left_value % right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value
