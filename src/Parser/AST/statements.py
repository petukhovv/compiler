from src.Compiler.VM import statements as compile_vm
from src.Interpreter import statements as interpreter

from pprint import pprint

"""
Assign statement class for AST.
eval - runtime function for Evaluator (return variable by name from environment).
Example: x := 56
"""
class AssignStatement:
    def __init__(self, variable, aexp):
        self.variable = variable
        self.aexp = aexp

    def eval(self, env):
        return interpreter.assign_statement(env, self.variable, self.aexp)

    def compile_vm(self, commands, env):
        return compile_vm.assign_statement(commands, env, self.variable, self.aexp)

"""
Compound statement class for AST.
eval - runtime function for Evaluator (eval first and second statement operators).
"""
class CompoundStatement:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def eval(self, env):
        return interpreter.compound_statement(env, self.first, self.second)

    def compile_vm(self, commands, env):
        return compile_vm.compound_statement(commands, env, self.first, self.second)

"""
'If' statement class for AST.
eval - runtime function for Evaluator (true of false statement depending on condition).
"""
class IfStatement:
    def __init__(self, condition, true_stmt, alternatives_stmt=None, false_stmt=None):
        self.condition = condition
        self.true_stmt = true_stmt
        self.alternatives_stmt = alternatives_stmt
        self.false_stmt = false_stmt

    def eval(self, env):
        return interpreter.if_statement(env, self.condition, self.true_stmt, self.alternatives_stmt, self.false_stmt)

    def compile_vm(self, commands, env, label_endif=None):
        return compile_vm.if_statement(commands, env, self.condition, self.true_stmt, self.alternatives_stmt, self.false_stmt, label_endif)

"""
'While' statement class for AST.
eval - runtime function for Evaluator (body eval while condition).
"""
class WhileStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def eval(self, env):
        return interpreter.while_statement(env, self.condition, self.body)

    def compile_vm(self, commands, env):
        return compile_vm.while_statement(commands, env, self.condition, self.body)

"""
'For' statement class for AST.
eval - runtime function for Evaluator ('for' loop).
"""
class ForStatement:
    def __init__(self, stmt1, stmt2, stmt3, body):
        self.stmt1 = stmt1
        self.stmt2 = stmt2
        self.stmt3 = stmt3
        self.body = body

    def eval(self, env):
        return interpreter.for_statement(env, self.stmt1, self.stmt2, self.stmt3, self.body)

    def compile_vm(self, commands, env):
        return compile_vm.for_statement(commands, env, self.stmt1, self.stmt2, self.stmt3, self.body)

"""
'Repeat' statement class for AST.
eval - runtime function for Evaluator (body eval while condition).
"""
class RepeatStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def eval(self, env):
        return interpreter.repeat_statement(env, self.condition, self.body)

    def compile_vm(self, commands, env):
        return compile_vm.repeat_statement(commands, env, self.condition, self.body)

"""
'Skip' statement class for AST.
eval - runtime function for Evaluator (empty function).
"""
class SkipStatement:

    def eval(self, env):
        return interpreter.skip_statement(env)

    def compile_vm(self, commands, env):
        return compile_vm.skip_statement(commands, env)
