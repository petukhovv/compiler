from src.Interpreter import common as interpreter

class Pointer:
    def __init__(self, env, element):
        self.env = env
        self.element = element

    def eval(self):
        return interpreter.pointer(self.env, self.element)

"""
'Enumeration' statement class for AST.
eval - runtime function for Evaluator (empty function).
"""
class Enumeration:
    def __init__(self, elements):
        self.elements = elements

    def eval(self):
        return interpreter.enumeration(self.elements)
