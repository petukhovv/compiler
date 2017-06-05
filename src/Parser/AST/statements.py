from src.Parser.AST.arrays import *

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
        value = self.aexp.eval(env)
        if isinstance(self.variable, ArrayElement):
            arr_descr = self.variable
            index = arr_descr.index.eval(env)
            arr = Environment(env).get(arr_descr.array)
            value_is_array = isinstance(self.aexp, UnboxedArrayWrap) or isinstance(self.aexp, BoxedArrayWrap)
            array_is_unboxed = isinstance(arr, UnboxedArrayWrap)
            if value_is_array or array_is_unboxed:
                arr[index] = value
            else:
                arr[index] = Pointer(env, self.aexp)
            Environment(env).set(arr_descr.array, arr)
        else:
            name = self.variable.name
            Environment(env).set(name, value)

"""
Compound statement class for AST.
eval - runtime function for Evaluator (eval first and second statement operators).
"""
class CompoundStatement:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)

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
        condition_value = self.condition.eval(env)
        if condition_value:
            self.true_stmt.eval(env)
        else:
            if self.alternatives_stmt:
                for alternative_stmt in self.alternatives_stmt:
                    alternative_condition_value = alternative_stmt.eval(env)
                    if alternative_condition_value:
                        return True
            if self.false_stmt:
                self.false_stmt.eval(env)
        return condition_value

"""
'While' statement class for AST.
eval - runtime function for Evaluator (body eval while condition).
"""
class WhileStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def eval(self, env):
        while self.condition.eval(env):
            self.body.eval(env)

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
        self.stmt1.eval(env)
        while self.stmt2.eval(env):
            iteration_env = Environment(env).create()
            self.body.eval(iteration_env)
            self.stmt3.eval(env)
        return

"""
'Repeat' statement class for AST.
eval - runtime function for Evaluator (body eval while condition).
"""
class RepeatStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def eval(self, env):
        while True:
            self.body.eval(env)
            condition_value = self.condition.eval(env)
            if condition_value:
                break

"""
'Skip' statement class for AST.
eval - runtime function for Evaluator (empty function).
"""
class SkipStatement:

    def eval(self, env):
        return
