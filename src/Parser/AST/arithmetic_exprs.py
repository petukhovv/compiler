from Compiler.ASM import arithmetic_exprs as compile_asm
from Compiler.VM import arithmetic_exprs as compile_vm
from Interpreter import arithmetic_exprs as interpreter

from .base import AST

CLASS = "arithmetic_exprs"


class IntAexp(AST):
    """
    Integer arithmetic expression class for AST.
    interpret - runtime function for Evaluator (just return i).
    Example: 54
    """
    def __init__(self, i):
        super().__init__(CLASS, "int_aexp")

        self.i = i

    def interpret(self, env):
        return interpreter.int_aexp(env, self.i)


class VarAexp(AST):
    """
    Variable arithmetic expression class for AST.
    interpret - runtime function for Evaluator (return variable from environment by name).
    Example: x
    """
    def __init__(self, name):
        super().__init__(CLASS, "var_aexp")

        self.name = name
        self.context = 'get'
        self.type = None

    def interpret(self, env):
        return interpreter.var_aexp(env, self.name)


class BinopAexp(AST):
    """
    Binary operation arithmetic expression class for AST.
    interpret - runtime function for Evaluator (return result of applying the aoperation to left and right values).
    Example: x + 54
    """
    def __init__(self, op, left, right):
        super().__init__(CLASS, "binop_aexp")

        self.op = op
        self.left = left
        self.right = right
        self.children = [left, right]

    def interpret(self, env):
        return interpreter.binop_aexp(env, self.op, self.left, self.right)
