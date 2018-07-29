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

