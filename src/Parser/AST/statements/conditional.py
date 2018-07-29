from ..base import AST

CLASS = "statements.conditional"


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
