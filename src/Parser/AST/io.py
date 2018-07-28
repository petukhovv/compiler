from Compiler.ASM import io as compile_asm
from Compiler.VM import io as compile_vm
from Interpreter import io as interpreter

from .base import AST

CLASS = "io"


class ReadStatement(AST):
    """
    'Read' statement class for AST.
    interpret - runtime function for Evaluator (get value from stdin).
    """
    def __init__(self):
        super().__init__(CLASS, "read_statement")

    def interpret(self, env):
        return interpreter.read_statement(env)

    def compile_vm(self, commands, data):
        return compile_vm.read_statement(commands, data)


class WriteStatement(AST):
    """
    'Write' statement class for AST.
    interpret - runtime function for Evaluator (write value to stdout).
    """
    def __init__(self, aexp):
        super().__init__(CLASS, "write_statement")

        self.aexp = aexp
        self.children = [aexp]

    def interpret(self, env):
        return interpreter.write_statement(env, self.aexp)

    def compile_vm(self, commands, data):
        return compile_vm.write_statement(commands, data, self.aexp)
