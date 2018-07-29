from ...Helpers.environment import Environment


def call_statement(env, node):
    """
    'Function call' statement def for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    fun = env['f'][node.name]
    func_env = Environment(env).create(env['f'])
    args = fun['args'].interpret(env)
    call_args_interpretuated = node.args.interpret(env)
    args_counter = 0
    for arg in args:
        func_env['v'][arg] = call_args_interpretuated[args_counter].interpret(env)
        args_counter += 1
    fun['body'].interpret(func_env)
    return func_env['r']
