from Compiler.VM.Codegen.declarations import object as compile_vm
from Compiler.ASM.Codegen.declarations import object as compile_asm
from Interpreter.Eval.declarations import object as interpreter

from ..base import AST

CLASS = "declarations.object"


class Object(AST):
    def __init__(self, elements):
        super().__init__(CLASS, "object_def")

        self.elements = elements
        self.children = [elements]
