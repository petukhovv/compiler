from Compiler.VM import common as compile_vm
from Interpreter import common as interpreter
from pprint import pprint


class Pointer:
    def __init__(self, env, element):
        self.env = env
        self.element = element

    def eval(self):
        return interpreter.pointer(self.env, self.element)


class Enumeration:
    """
    'Enumeration' statement class for AST.
    eval - runtime function for Evaluator (empty function).
    """
    def __init__(self, elements):
        self.elements = elements

    def eval(self):
        return interpreter.enumeration(self.elements)

    def compile_vm(self, commands, data):
        return compile_vm.enumeration(commands, data, self.elements)
