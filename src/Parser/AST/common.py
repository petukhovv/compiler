from src.Compiler.VM import common as compile_vm
from src.Interpreter import common as interpreter
from pprint import pprint

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

    def compile_vm(self, commands, env):
        return compile_vm.enumeration(commands, env, self.elements)
