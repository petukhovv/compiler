from Compiler.ASM import boolean_exprs as compile_asm
from Compiler.VM import boolean_exprs as compile_vm
from Interpreter import boolean_exprs as interpreter


class RelopBexp:
    """
    Relation operation boolean expression class for AST.
    interpret - runtime function for Evaluator (return result of applying the boolean operation to left and right values).
    Example: x > 56
    """
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def interpret(self, env):
        return interpreter.relop_bexp(env, self.op, self.left, self.right)

    def compile_vm(self, commands, data):
        return compile_vm.relop_bexp(commands, data, self.op, self.left, self.right)

    def compile_asm(self, compiler):
        return compile_asm.relop_bexp(compiler, self.op, self.left, self.right)


class AndBexp:
    """
    'And' operation boolean expression class for AST.
    interpret - runtime function for Evaluator (return result of applying the 'and' operation to left and right values).
    Example: x > 56 and x < 61
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def interpret(self, env):
        return interpreter.and_bexp(env, self.left, self.right)

    def compile_vm(self, commands, data):
        return compile_vm.and_bexp(commands, data, self.left, self.right)

    def compile_asm(self, compiler):
        return compile_asm.and_bexp(compiler, self.left, self.right)


class OrBexp:
    """
    'Or' operation boolean expression class for AST.
    interpret - runtime function for Evaluator (return result of applying the 'or' operation to left and right values).
    Example: x < 11 or x > 100
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def interpret(self, env):
        return interpreter.or_bexp(env, self.left, self.right)

    def compile_vm(self, commands, data):
        return compile_vm.or_bexp(commands, data, self.left, self.right)

    def compile_asm(self, compiler):
        return compile_asm.or_bexp(compiler, self.left, self.right)


class NotBexp:
    """
    'Not' operation boolean expression class for AST.
    interpret - runtime function for Evaluator (return result of applying the 'not' operation to value).
    Example: x not 11
    """
    def __init__(self, exp):
        self.exp = exp

    def interpret(self, env):
        return interpreter.not_bexp(env, self.exp)

    def compile_vm(self, commands, data):
        return compile_vm.not_bexp(commands, data, self.exp)

    def compile_asm(self, compiler):
        return compile_asm.not_bexp(compiler, self.exp)
