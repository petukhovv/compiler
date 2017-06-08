from Helpers.environment import *

"""
'Function' statement def for AST.
eval - runtime function for Evaluator (empty function).
"""
def function(env, name, args, body):
    env['f'][name] = {
        'args': args,
        'body': body
    }

"""
'Return' statement def for AST.
eval - runtime function for Evaluator (empty function).
"""
def return_statement(env, expr):
    env['r'] = expr.eval(env)
    return

"""
'Function call' statement def for AST.
eval - runtime function for Evaluator (empty function).
"""
def function_call_statement(env, name, call_args):
    fun = env['f'][name]
    func_env = Environment(env).create(env['f'])
    args = fun['args'].eval()
    call_args_evaluated = call_args.eval()
    args_counter = 0
    for arg in args:
        func_env['v'][arg] = call_args_evaluated[args_counter].eval(env)
        args_counter += 1
    fun['body'].eval(func_env)
    return func_env['r']
