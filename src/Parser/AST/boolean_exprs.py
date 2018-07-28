from Compiler.ASM import boolean_exprs as compile_asm
from Compiler.VM import boolean_exprs as compile_vm
from Interpreter import boolean_exprs as interpreter

from .base import AST

CLASS = "boolean_exprs"


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

    def interpret(self, env):
        return interpreter.relop_bexp(env, self.op, self.left, self.right)


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

    def interpret(self, env):
        return interpreter.and_bexp(env, self.left, self.right)


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

    def interpret(self, env):
        return interpreter.or_bexp(env, self.left, self.right)


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

    def interpret(self, env):
        return interpreter.not_bexp(env, self.exp)
