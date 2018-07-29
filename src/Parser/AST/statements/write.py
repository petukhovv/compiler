from Compiler.ASM.Codegen.statements import write as compile_asm
from Compiler.VM.Codegen.statements import write as compile_vm
from Interpreter.Eval.statements import write as interpreter

from ..base import AST

CLASS = "statements.write"


class WriteStatement(AST):
    """
    'Write' statement class for AST.
    interpret - runtime function for Evaluator (write value to stdout).
    """
    def __init__(self, aexp):
        super().__init__(CLASS, "write_statement")

        self.aexp = aexp
        self.children = [aexp]
