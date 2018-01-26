from Interpreter.Helpers.environment import *

from Compiler.VM import functions as compile_vm
from Compiler.ASM import functions as compile_asm
from Interpreter import functions as interpreter


class Function:
    """
    'Function' statement class for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body

    def interpret(self, env):
        return interpreter.function(env, self.name, self.args, self.body)

    def compile_vm(self, commands, data):
        return compile_vm.function(commands, data, self.name, self.args, self.body)

    def compile_asm(self, compiler):
        return compile_asm.function(compiler, self.name, self.args, self.body)


class ReturnStatement:
    """
    'Return' statement class for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    def __init__(self, expr):
        self.expr = expr

    def interpret(self, env):
        return interpreter.return_statement(env, self.expr)

    def compile_vm(self, commands, data):
        return compile_vm.return_statement(commands, data, self.expr)

    def compile_asm(self, compiler):
        return compile_asm.return_statement(compiler, self.expr)


class FunctionCallStatement:
    """
    'Function call' statement class for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def interpret(self, env):
        fun = env['f'][self.name]
        func_env = Environment(env).create(env['f'])
        args = fun['args'].interpret()
        call_args_interpretuated = self.args.interpret()
        args_counter = 0
        for arg in args:
            func_env['v'][arg] = call_args_interpretuated[args_counter].interpret(env)
            args_counter += 1
        fun['body'].interpret(func_env)
        return func_env['r']

    def compile_vm(self, commands, data):
        return compile_vm.call_statement(commands, data, self.name, self.args)

    def compile_asm(self, compiler):
        return compile_asm.call_statement(compiler, self.name, self.args)
