from Compiler.VM.Codegen.declarations import function as compile_vm
from Compiler.ASM.Codegen.declarations import function as compile_asm
from Interpreter.Eval.declarations import function as interpreter

from ..base import AST

CLASS = "declarations.function"


class Function(AST):
    """
    'Function' statement class for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    def __init__(self, name, args, body):
        super().__init__(CLASS, "function")

        self.name = name
        self.args = args
        self.body = body
        self.children = [args, body]
