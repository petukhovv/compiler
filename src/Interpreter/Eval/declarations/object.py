from ...Helpers.environment import Environment
from ...Helpers.objects import ObjectWrap


def object_def(env, node):
    obj_env = Environment(env).create()
    obj = ObjectWrap(obj_env)
    Environment.context_objects.append(obj)

    for element in node.elements.elements:
        element.interpret(obj_env)

    return obj
