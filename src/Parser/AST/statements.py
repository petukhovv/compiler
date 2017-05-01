import sys

from equality import *

"""
Base class for statement classes.
"""
class Statement(Equality):
    pass

"""
Assign statement class for AST.
eval - runtime function for Evaluator (return variable by name from environment).
Example: x := 56
"""
class AssignStatement(Statement):
    def __init__(self, name, aexp):
        self.name = name
        self.aexp = aexp

    def __repr__(self):
        return 'AssignStatement(%s, %s)' % (self.name, self.aexp)

    def eval(self, env):
        value = self.aexp.eval(env)
        env[self.name] = value

"""
Compound statement class for AST.
eval - runtime function for Evaluator (eval first and second statement operators).
"""
class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return 'CompoundStatement(%s, %s)' % (self.first, self.second)

    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)

"""
'If' statement class for AST.
eval - runtime function for Evaluator (true of false statement depending on condition).
"""
class IfStatement(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt

    def __repr__(self):
        return 'IfStatement(%s, %s, %s)' % (self.condition, self.true_stmt, self.false_stmt)

    def eval(self, env):
        condition_value = self.condition.eval(env)
        if condition_value:
            self.true_stmt.eval(env)
        else:
            if self.false_stmt:
                self.false_stmt.eval(env)

"""
'While' statement class for AST.
eval - runtime function for Evaluator (body eval while condition).
"""
class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'WhileStatement(%s, %s)' % (self.condition, self.body)

    def eval(self, env):
        condition_value = self.condition.eval(env)
        while condition_value:
            self.body.eval(env)
            condition_value = self.condition.eval(env)

"""
'Read' statement class for AST.
eval - runtime function for Evaluator (get value from stdin).
"""
class ReadStatement(Statement):
    def __repr__(self):
        return 'ReadStatement'

    def eval(self, env):
        value = sys.stdin.readline()
        try:
            return int(value)
        except ValueError:
            raise RuntimeError(value + ' is not integer')

"""
'Write' statement class for AST.
eval - runtime function for Evaluator (write value to stdout).
"""
class WriteStatement(Statement):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'WriteStatement(%s)' % self.name

    def eval(self, env):
        try:
            value = env[self.name]
            sys.stdout.write(str(value) + '\n')
        except KeyError:
            raise RuntimeError(self.name + ' is not defined')
        return
