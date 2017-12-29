from .Helpers.environment import *


def function(env, name, args, body):
    """
    'Function' statement def for AST.
    eval - runtime function for Evaluator (empty function).
    """
    env['f'][name] = {
        'args': args,
        'body': body
    }


def return_statement(env, expr):
    """
    'Return' statement def for AST.
    eval - runtime function for Evaluator (empty function).
    """
    env['r'] = expr.eval(env)
    return


def function_call_statement(env, name, call_args):
    """
    'Function call' statement def for AST.
    eval - runtime function for Evaluator (empty function).
    """
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
