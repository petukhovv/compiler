from src.Compiler.VM import arithmetic_exprs as compile_vm
from src.Interpreter import arithmetic_exprs as interpreter

"""
Integer arithmetic expression class for AST.
eval - runtime function for Evaluator (just return i).
Example: 54
"""
class IntAexp:
    def __init__(self, i):
        self.i = i

    def eval(self, env):
        return interpreter.int_aexp(env, self.i)

    def compile_vm(self, commands, env):
        return compile_vm.int_aexp(commands, env, self.i)

"""
Variable arithmetic expression class for AST.
eval - runtime function for Evaluator (return variable from environment by name).
Example: x
"""
class VarAexp:
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        return interpreter.var_aexp(env, self.name)

    def compile_vm(self, commands, env):
        return compile_vm.var_aexp(commands, env, self.name)

"""
Binary operation arithmetic expression class for AST.
eval - runtime function for Evaluator (return result of applying the aoperation to left and right values).
Example: x + 54
"""
class BinopAexp:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, env):
        return interpreter.binop_aexp(env, self.op, self.left, self.right)

    def compile_vm(self, commands, env):
        return compile_vm.binop_aexp(commands, env, self.op, self.left, self.right)
