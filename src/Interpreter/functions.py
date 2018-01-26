from .Helpers.environment import *


def function(env, name, args, body):
    """
    'Function' statement def for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    env['f'][name] = {
        'args': args,
        'body': body
    }


def return_statement(env, expr):
    """
    'Return' statement def for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    env['r'] = expr.interpret(env)
    return


def function_call_statement(env, name, call_args):
    """
    'Function call' statement def for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    fun = env['f'][name]
    func_env = Environment(env).create(env['f'])
    args = fun['args'].interpret()
    call_args_interpretuated = call_args.interpret()
    args_counter = 0
    for arg in args:
        func_env['v'][arg] = call_args_interpretuated[args_counter].interpret(env)
        args_counter += 1
    fun['body'].interpret(func_env)
    return func_env['r']
