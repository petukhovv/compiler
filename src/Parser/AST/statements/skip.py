from ..base import AST

CLASS = "statements.skip"


class SkipStatement(AST):
    def __init__(self):
        super().__init__(CLASS, "skip_statement")
