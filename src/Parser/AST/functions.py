from Compiler.VM import functions as compile_vm
from Compiler.ASM import functions as compile_asm
from Interpreter import functions as interpreter

from .base import AST

CLASS = "functions"


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


class ReturnStatement(AST):
    """
    'Return' statement class for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    def __init__(self, expr):
        super().__init__(CLASS, "return_statement")

        self.expr = expr
        self.children = [expr]


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
