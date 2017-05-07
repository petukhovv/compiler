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
        env['v'][self.name] = value

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
        while self.condition.eval(env):
            self.body.eval(env)

"""
'For' statement class for AST.
eval - runtime function for Evaluator ('for' loop).
"""
class ForStatement(Statement):
    def __init__(self, stmt1, stmt2, stmt3, body):
        self.stmt1 = stmt1
        self.stmt2 = stmt2
        self.stmt3 = stmt3
        self.body = body

    def __repr__(self):
        return 'ForStatement(%s, %s, %s, %s)' % (self.stmt1, self.stmt2, self.stmt3, self.body)

    def eval(self, env):
        self.stmt1.eval(env)
        while self.stmt2.eval(env):
            self.body.eval(env)
            self.stmt3.eval(env)
        return

"""
'Repeat' statement class for AST.
eval - runtime function for Evaluator (body eval while condition).
"""
class RepeatStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'RepeatStatement(%s, %s)' % (self.condition, self.body)

    def eval(self, env):
        while True:
            self.body.eval(env)
            condition_value = self.condition.eval(env)
            if condition_value:
                break

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
    def __init__(self, aexp):
        self.aexp = aexp

    def __repr__(self):
        return 'WriteStatement(%s)' % self.aexp

    def eval(self, env):
        value = self.aexp.eval(env)
        if type(value) is bool:
            value = int(value)
        sys.stdout.write(str(value) + '\n')

"""
'Skip' statement class for AST.
eval - runtime function for Evaluator (empty function).
"""
class SkipStatement(Statement):
    def __repr__(self):
        return 'SkipStatement(%s)'

    def eval(self, env):
        return

"""
'Arguments' statement class for AST.
eval - runtime function for Evaluator (empty function).
"""
class ArgumentsStatement(Statement):
    def __init__(self, arguments):
        self.arguments = arguments

    def __repr__(self):
        return 'ArgumentsStatement(%s)' % self.arguments

    def eval(self):
        return self.arguments

"""
'Function' statement class for AST.
eval - runtime function for Evaluator (empty function).
"""
class FunctionStatement(Statement):
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body

    def __repr__(self):
        return 'FunctionStatement(%s, %s, %s)' % (self.name, self.args, self.body)

    def eval(self, env):
        env['f'][self.name] = {
            'env': {
                'v': {},
                'f': {},
                'r': None
            },
            'args': self.args,
            'body': self.body
        }
        return

"""
'Return' statement class for AST.
eval - runtime function for Evaluator (empty function).
"""
class ReturnStatement(Statement):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return 'ReturnStatement(%s)' % self.expr

    def eval(self, env):
        env['r'] = self.expr.eval(env)
        return

"""
'Function call' statement class for AST.
eval - runtime function for Evaluator (empty function).
"""
class FunctionCallStatement(Statement):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return 'FunctionCallStatement(%s, %s)' % (self.name, self.args)

    def eval(self, env):
        fun = env['f'][self.name]
        func_env = fun['env']
        args = fun['args'].eval()
        call_args = self.args.eval()
        args_counter = 0
        for arg in args:
            func_env['v'][arg] = env['v'][call_args[args_counter]]
            args_counter += 1
        fun['body'].eval(func_env)
        return func_env['r']
