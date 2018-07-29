from Compiler.ASM.Codegen.statements import assignment as compile_asm
from Compiler.VM.Codegen.statements import assignment as compile_vm
from Interpreter.Eval.statements import assignment as interpreter

from ..base import AST

CLASS = "statements.assignment"


class AssignmentStatement(AST):
    """
    Assign statement class for AST.
    interpret - runtime function for Evaluator (return variable by name from environment).
    Example: x := 56
    """
    def __init__(self, variable, aexp):
        super().__init__(CLASS, "assign_statement")

        self.variable = variable
        self.aexp = aexp
        self.children = [variable, aexp]