from Compiler.ASM.Codegen.statements import loop as compile_asm
from Compiler.VM.Codegen.statements import loop as compile_vm
from Interpreter.Eval.statements import loop as interpreter

from ..base import AST

CLASS = "statements.loop"


class WhileStatement(AST):
    """
    'While' statement class for AST.
    interpret - runtime function for Evaluator (body interpret while condition).
    """
    def __init__(self, condition, body):
        super().__init__(CLASS, "while_statement")

        self.condition = condition
        self.body = body
        self.children = [body, condition]


class ForStatement(AST):
    """
    'For' statement class for AST.
    interpret - runtime function for Evaluator ('for' loop).
    """
    def __init__(self, stmt1, stmt2, stmt3, body):
        super().__init__(CLASS, "for_statement")

        self.stmt1 = stmt1
        self.stmt2 = stmt2
        self.stmt3 = stmt3
        self.body = body
        self.children = [stmt1, stmt2, stmt3, body]


class RepeatStatement(AST):
    """
    'Repeat' statement class for AST.
    interpret - runtime function for Evaluator (body interpret while condition).
    """
    def __init__(self, condition, body):
        super().__init__(CLASS, "repeat_statement")

        self.condition = condition
        self.body = body
        self.children = [condition, body]

