from .Helpers.environment import *
from .Helpers.common import BoxedArrayWrap, UnboxedArrayWrap


class ObjectWrap:
    def __init__(self, env):
        self.env = env

    def get_var(self, name):
        return self.env['v'][name]

    def get_method(self, name):
        return self.env['f'][name]

    def set(self, name, value):
        self.env['v'][name] = value


def object_def(env, elements):
    obj_env = Environment(env).create()
    obj = ObjectWrap(obj_env)
    Environment.context_objects.append(obj)

    for element in elements.elements:
        element.interpret(obj_env)

    return obj


def object_val_def(env, variable, value):
    value = value.interpret(env)
    Environment(env).set(variable.name, value)

    return value


def object_val(env, object_name, prop_name, other_prop_names):
    obj = Environment(env).get(object_name)
    value = obj.get_var(prop_name)

    if other_prop_names:
        for other_prop_name in other_prop_names:
            if isinstance(value, UnboxedArrayWrap) or isinstance(value, BoxedArrayWrap):
                other_index = other_prop_name.interpret(value.env)
                value = value[other_index]
            else:
                value = value.get_var(other_prop_name)

    return value


def object_method(env, object_name, method_name, call_args):
    obj = Environment(env).get(object_name)
    func_env = Environment(env).create(env['f'])
    method = obj.get_method(method_name)
    args = method['args'].interpret()
    call_args_interpreted = call_args.interpret()

    args_counter = 0
    for arg in args:
        func_env['v'][arg] = call_args_interpreted[args_counter].interpret(env)
        args_counter += 1
    method['body'].interpret(func_env)
    return func_env['r']
