from src.Parser.helpers import *

"""
Integer arithmetic expression class for AST.
eval - runtime function for Evaluator (just return i).
Example: 54
"""
class IntAexp:
    def __init__(self, i):
        self.i = i

    def eval(self, env):
        return self.i

"""
Variable arithmetic expression class for AST.
eval - runtime function for Evaluator (return variable from environment by name).
Example: x
"""
class VarAexp:
    pointers = 0

    def __init__(self, name):
        self.name = name

    def eval(self, env):
        return Environment(env).get(self.name)

"""
Binary operation arithmetic expression class for AST.
eval - runtime function for Evaluator (return result of applying the aoperation to left and right values).
Example: x + 54
"""
class BinopAexp:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

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
