from Compiler.VM import common as compile_vm
from Compiler.ASM import common as compile_asm
from Interpreter import common as interpreter


class Pointer:
    def __init__(self, env, element):
        self.env = env
        self.element = element
        self.children = [element]

    def interpret(self):
        return interpreter.pointer(self.env, self.element)


class Enumeration:
    """
    'Enumeration' statement class for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    def __init__(self, elements):
        self.elements = elements
        self.children = elements

    def interpret(self):
        return interpreter.enumeration(self.elements)

    def compile_vm(self, commands, data):
        return compile_vm.enumeration(commands, data, self.elements)

    def compile_asm(self, compiler):
        return compile_asm.enumeration(compiler, self.elements)
