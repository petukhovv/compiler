from equality import *

"""
Base class for common AST-classes.
"""
class CommonBase(Equality):
    pass

"""
'Enumeration' statement class for AST.
eval - runtime function for Evaluator (empty function).
"""
class Enumeration(CommonBase):
    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        return 'Enumeration(%s)' % self.elements

    def eval(self):
        return self.elements
