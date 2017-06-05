class Pointer:
    def __init__(self, env, element):
        self.env = env
        self.element = element

    def eval(self):
        return self.element.eval(self.env)

"""
'Enumeration' statement class for AST.
eval - runtime function for Evaluator (empty function).
"""
class Enumeration:
    def __init__(self, elements):
        self.elements = elements

    def eval(self):
        return self.elements
