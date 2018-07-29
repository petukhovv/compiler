from Compiler.ASM.Codegen import common as compile_asm
from Compiler.VM.Codegen import common as compile_vm
from Interpreter.Eval import common as interpreter

from .base import AST

CLASS = "common"


class CompoundStatement(AST):
    """
    Compound statement class for AST.
    interpret - runtime function for Evaluator (interpret first and second statement operators).
    """
    def __init__(self, first, second):
        super().__init__(CLASS, "compound_statement")

        self.first = first
        self.second = second
        self.children = [first, second]


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
