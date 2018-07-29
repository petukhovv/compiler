from ...Helpers.environment import Environment
from ...Helpers.common import BoxedArrayWrap, UnboxedArrayWrap


def object_val(env, node):
    if node.object_name == 'this':
        value = Environment.context_objects[-1].get_var(node.prop_name)
    else:
        obj = Environment(env).get(node.object_name)
        value = obj.get_var(node.prop_name)

    if node.other_prop_names:
        for other_prop_name in node.other_prop_names:
            if isinstance(value, UnboxedArrayWrap) or isinstance(value, BoxedArrayWrap):
                other_index = other_prop_name.interpret(value.env)
                value = value[other_index]
            else:
                value = value.get_var(other_prop_name)

    return value


def object_method(env, node):
    if node.object_name == 'this':
        method = Environment.context_objects[-1].get_method(node.method_name)
    else:
        obj = Environment(env).get(node.object_name)
        method = obj.get_method(node.method_name)

    func_env = Environment(env).create(env['f'])
    args = method['args'].interpret()
    call_args_interpreted = node.call_args.interpret()

    args_counter = 0
    for arg in args:
        func_env['v'][arg] = call_args_interpreted[args_counter].interpret(env)
        args_counter += 1
    method['body'].interpret(func_env)
    return func_env['r']
