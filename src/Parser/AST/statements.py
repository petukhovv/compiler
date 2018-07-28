from Compiler.ASM import statements as compile_asm
from Compiler.VM import statements as compile_vm
from Interpreter import statements as interpreter

from .base import AST

CLASS = "statements"


class AssignStatement(AST):
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


class CompoundStatement(AST):
    """
    Compound statement class for AST.
    interpret - runtime function for Evaluator (interpret first and second statement operators).
    """
    def __init__(self, first, second):
        super().__init__(CLASS, "compound_statement")

        self.first = first
        self.second = second
        self.children = [first, second]


class IfStatement(AST):
    """
    'If' statement class for AST.
    interpret - runtime function for Evaluator (true of false statement depending on condition).
    """
    def __init__(self, condition, true_stmt, alternatives_stmt=None, false_stmt=None, label_endif=None):
        super().__init__(CLASS, "if_statement")

        self.condition = condition
        self.true_stmt = true_stmt
        self.alternatives_stmt = alternatives_stmt
        self.false_stmt = false_stmt
        self.children = [condition, true_stmt, alternatives_stmt, false_stmt]
        self.label_endif = label_endif


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


class SkipStatement(AST):
    def __init__(self):
        super().__init__(CLASS, "skip_statement")
