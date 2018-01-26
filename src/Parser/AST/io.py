from Compiler.ASM import io as compile_asm
from Compiler.VM import io as compile_vm
from Interpreter import io as interpreter


class ReadStatement:
    """
    'Read' statement class for AST.
    eval - runtime function for Evaluator (get value from stdin).
    """
    def __init__(self): pass

    def eval(self, env):
        return interpreter.read_statement(env)

    def compile_vm(self, commands, data):
        return compile_vm.read_statement(commands, data)

    def compile_asm(self, compiler):
        return compile_asm.read_statement(compiler)


class WriteStatement:
    """
    'Write' statement class for AST.
    eval - runtime function for Evaluator (write value to stdout).
    """
    def __init__(self, aexp):
        self.aexp = aexp

    def eval(self, env):
        return interpreter.write_statement(env, self.aexp)

    def compile_vm(self, commands, data):
        return compile_vm.write_statement(commands, data, self.aexp)

    def compile_asm(self, compiler):
        return compile_asm.write_statement(compiler, self.aexp)
