from Compiler.VM import common as compile_vm
from Compiler.ASM import common as compile_asm
from Interpreter import common as interpreter

from .base import AST

CLASS = "common"


class Pointer(AST):
    def __init__(self, env, element):
        super().__init__(CLASS, "pointer")

        self.env = env
        self.element = element
        self.children = [element]


class Enumeration(AST):
    """
    'Enumeration' statement class for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    def __init__(self, elements):
        super().__init__(CLASS, "enumeration")

        self.elements = elements
        self.children = elements
