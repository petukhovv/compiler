

"""
Base class for statement classes.
"""
class FunctionBase:
    pass

"""
'Function' statement class for AST.
eval - runtime function for Evaluator (empty function).
"""
class Function(FunctionBase):
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body

    def __repr__(self):
        return 'Function(%s, %s, %s)' % (self.name, self.args, self.body)

    def eval(self, env):
        env['f'][self.name] = {
            'args': self.args,
            'body': self.body
        }

"""
'Return' statement class for AST.
eval - runtime function for Evaluator (empty function).
"""
class ReturnStatement(FunctionBase):
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
class FunctionCallStatement(FunctionBase):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return 'FunctionCallStatement(%s, %s)' % (self.name, self.args)

    def eval(self, env):
        fun = env['f'][self.name]
        func_env = {
            'v': {},
            'f': env['f'],
            'r': None
        }
        args = fun['args'].eval()
        call_args = self.args.eval()
        args_counter = 0
        for arg in args:
            func_env['v'][arg] = call_args[args_counter].eval(env)
            args_counter += 1
        fun['body'].eval(func_env)
        return func_env['r']
