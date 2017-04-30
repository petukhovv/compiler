from equality import *

"""
Base class for boolean expression classes.
"""
class Bexp(Equality):
    pass

"""
Relation operation boolean expression class for AST.
Example: x > 56
"""
class RelopBexp(Bexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return 'RelopBexp(%s, %s, %s)' % (self.op, self.left, self.right)

"""
'And' operation boolean expression class for AST.
Example: x > 56 and x < 61
"""
class AndBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'AndBexp(%s, %s)' % (self.left, self.right)

"""
'Or' operation boolean expression class for AST.
Example: x < 11 or x > 100
"""
class OrBexp(Bexp):
        def __init__(self, left, right):
            self.left = left
            self.right = right

        def __repr__(self):
            return 'OrBexp(%s, %s)' % (self.left, self.right)

"""
'Not' operation boolean expression class for AST.
Example: x not 11
"""
class NotBexp(Bexp):
    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return 'NotBexp(%s)' % self.exp

    def eval(self, env):
        value = self.exp.eval(env)
        return not value
