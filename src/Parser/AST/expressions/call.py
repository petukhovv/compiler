from Compiler.VM.Codegen.expressions import call as compile_vm
from Compiler.ASM.Codegen.expressions import call as compile_asm
from Interpreter.Eval.expressions import call as interpreter

from ..base import AST

CLASS = "expressions.call"


class FunctionCallStatement(AST):
    """
    'Function call' statement class for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    def __init__(self, name, args):
        super().__init__(CLASS, "call_statement")

        self.name = name
        self.args = args
        self.children = [args]
