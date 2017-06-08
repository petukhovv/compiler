from src.Interpreter import io as interpreter

"""
'Read' statement class for AST.
eval - runtime function for Evaluator (get value from stdin).
"""
class ReadStatement:
    def __repr__(self):
        return 'ReadStatement'

    def eval(self, env):
        return interpreter.read_statement(env)

"""
'Write' statement class for AST.
eval - runtime function for Evaluator (write value to stdout).
"""
class WriteStatement:
    def __init__(self, aexp):
        self.aexp = aexp

    def eval(self, env):
        return interpreter.write_statement(env, self.aexp)
