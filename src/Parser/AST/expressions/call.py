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
