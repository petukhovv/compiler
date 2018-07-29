from ...Helpers.environment import Environment


def object_val_def(env, node):
    value = node.value.interpret(env)
    Environment(env).set(node.variable.name, value)

    return value
