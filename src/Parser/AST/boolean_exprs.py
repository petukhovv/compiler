"""
Relation operation boolean expression class for AST.
eval - runtime function for Evaluator (return result of applying the boolean operation to left and right values).
Example: x > 56
"""
class RelopBexp:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '<':
            value = left_value < right_value
        elif self.op == '<=':
            value = left_value <= right_value
        elif self.op == '>':
            value = left_value > right_value
        elif self.op == '>=':
            value = left_value >= right_value
        elif self.op == '==':
            value = left_value == right_value
        elif self.op == '!=':
            value = left_value != right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value

"""
'And' operation boolean expression class for AST.
eval - runtime function for Evaluator (return result of applying the 'and' operation to left and right values).
Example: x > 56 and x < 61
"""
class AndBexp:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value and right_value

"""
'Or' operation boolean expression class for AST.
eval - runtime function for Evaluator (return result of applying the 'or' operation to left and right values).
Example: x < 11 or x > 100
"""
class OrBexp:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value or right_value

"""
'Not' operation boolean expression class for AST.
eval - runtime function for Evaluator (return result of applying the 'not' operation to value).
Example: x not 11
"""
class NotBexp:
    def __init__(self, exp):
        self.exp = exp

    def eval(self, env):
        value = self.exp.eval(env)
        return not value
