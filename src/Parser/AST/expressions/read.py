from Compiler.ASM.Codegen.expressions import read as compile_asm
from Compiler.VM.Codegen.expressions import read as compile_vm
from Interpreter.Eval.expressions import read as interpreter

from ..base import AST

CLASS = "expressions.read"


class ReadStatement(AST):
    """
    'Read' statement class for AST.
    interpret - runtime function for Evaluator (get value from stdin).
    """
    def __init__(self):
        super().__init__(CLASS, "read_statement")

