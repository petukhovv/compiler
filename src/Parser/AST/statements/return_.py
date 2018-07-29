from Compiler.VM.Codegen.statements import return_ as compile_vm
from Compiler.ASM.Codegen.statements import return_ as compile_asm
from Interpreter.Eval.statements import return_ as interpreter

from ..base import AST

CLASS = "statements.return_"


class ReturnStatement(AST):
    """
    'Return' statement class for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    def __init__(self, expr):
        super().__init__(CLASS, "return_statement")

        self.expr = expr
        self.children = [expr]

