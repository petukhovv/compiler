from ...Helpers.environment import Environment


def strset(env, node):
    args_node = node.args.interpret(env)
    if len(args_node) < 3:
        raise RuntimeError('strset is not call with three arguments')
    str = args_node[0].interpret(env)
    var_name = args_node[0].name
    char_index = args_node[1].interpret(env)
    if char_index < 0 or char_index >= len(str):
        raise RuntimeError('strset: incorrect index')
    new_char = args_node[2].interpret(env)
    new_str = list(str)
    new_str[char_index] = chr(new_char)
    Environment(env).set(var_name, "".join(new_str))
