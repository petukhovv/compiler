from Compiler.ASM.Codegen.statements import strings as compile_asm
from Compiler.VM.Codegen.statements import strings as compile_vm
from Interpreter.Eval.statements import strings as interpreter

from Parser.AST.base import AST

CLASS = "statements.strings"


class StrSet(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strset")

        self.args = args
        self.children = [args]
