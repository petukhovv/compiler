from Interpreter.Helpers.environment import *

from Compiler.VM import functions as compile_vm
from Compiler.ASM import functions as compile_asm
from Interpreter import functions as interpreter

from .base import AST

CLASS = "functions"


class Function(AST):
    """
    'Function' statement class for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    def __init__(self, name, args, body):
        super().__init__(CLASS, "function")

        self.name = name
        self.args = args
        self.body = body
        self.children = [args, body]

    def interpret(self, env):
        return interpreter.function(env, self.name, self.args, self.body)


class ReturnStatement(AST):
    """
    'Return' statement class for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    def __init__(self, expr):
        super().__init__(CLASS, "return_statement")

        self.expr = expr
        self.children = [expr]

    def interpret(self, env):
        return interpreter.return_statement(env, self.expr)


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
