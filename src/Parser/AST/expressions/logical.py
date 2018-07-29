from Parser.AST.base import AST

CLASS = "expressions.logical"


class RelopBexp(AST):
    """
    Relation operation boolean expression class for AST.
    interpret - runtime function for Evaluator (return result of applying the boolean operation to left and right values).
    Example: x > 56
    """
    def __init__(self, op, left, right):
        super().__init__(CLASS, "relop_bexp")

        self.op = op
        self.left = left
        self.right = right
        self.children = [left, right]


class AndBexp(AST):
    """
    'And' operation boolean expression class for AST.
    interpret - runtime function for Evaluator (return result of applying the 'and' operation to left and right values).
    Example: x > 56 and x < 61
    """
    def __init__(self, left, right):
        super().__init__(CLASS, "and_bexp")

        self.left = left
        self.right = right
        self.children = [left, right]


class OrBexp(AST):
    """
    'Or' operation boolean expression class for AST.
    interpret - runtime function for Evaluator (return result of applying the 'or' operation to left and right values).
    Example: x < 11 or x > 100
    """
    def __init__(self, left, right):
        super().__init__(CLASS, "or_bexp")

        self.left = left
        self.right = right
        self.children = [left, right]


class NotBexp(AST):
    """
    'Not' operation boolean expression class for AST.
    interpret - runtime function for Evaluator (return result of applying the 'not' operation to value).
    Example: x not 11
    """
    def __init__(self, exp):
        super().__init__(CLASS, "not_bexp")

        self.exp = exp
        self.children = [exp]
