from Compiler.ASM.Codegen.statements import skip as compile_asm
from Compiler.VM.Codegen.statements import skip as compile_vm
from Interpreter.Eval.statements import skip as interpreter

from ..base import AST

CLASS = "statements.skip"


class SkipStatement(AST):
    def __init__(self):
        super().__init__(CLASS, "skip_statement")
