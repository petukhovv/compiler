"""
Base class for common AST-classes.
"""
class CommonBase:
    pass

class Pointer(CommonBase):
    def __init__(self, env, element):
        self.env = env
        self.element = element

    def __repr__(self):
        return 'Pointer(%s, %s)' % (self.env, self.element)

    def eval(self):
        return self.element.eval(self.env)

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
