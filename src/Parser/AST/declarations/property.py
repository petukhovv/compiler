from Compiler.VM.Codegen.declarations import property as compile_vm
from Compiler.ASM.Codegen.declarations import property as compile_asm
from Interpreter.Eval.declarations import property as interpreter

from ..base import AST

CLASS = "declarations.property"


class ObjectValDef(AST):
    def __init__(self, name, value):
        super().__init__(CLASS, "object_val_def")

        self.name = name
        self.value = value
        self.children = [name, value]