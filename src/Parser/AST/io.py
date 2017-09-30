from src.Compiler.X86 import io as compile_x86
from src.Compiler.VM import io as compile_vm
from src.Interpreter import io as interpreter

"""
'Read' statement class for AST.
eval - runtime function for Evaluator (get value from stdin).
"""
class ReadStatement:
    def __init__(self): pass

    def eval(self, env):
        return interpreter.read_statement(env)

    def compile_vm(self, commands, data):
        return compile_vm.read_statement(commands, data)

    def compile_x86(self, compiler):
        return compile_x86.read_statement(compiler)

"""
'Write' statement class for AST.
eval - runtime function for Evaluator (write value to stdout).
"""
class WriteStatement:
    def __init__(self, aexp):
        self.aexp = aexp

    def eval(self, env):
        return interpreter.write_statement(env, self.aexp)

    def compile_vm(self, commands, data):
        return compile_vm.write_statement(commands, data, self.aexp)

    def compile_x86(self, compiler):
        return compile_x86.write_statement(compiler, self.aexp)
