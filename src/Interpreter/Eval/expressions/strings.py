def char(env, node):
    return ord(node.character)


def string(env, node):
    return node.characters


def strlen(env, node):
    args_node = node.args.interpret(env)
    if len(args_node) == 0:
        raise RuntimeError('strlen call without arguments')
    str = args_node[0].interpret(env)
    return len(str)


def strget(env, node):
    args_node = node.args.interpret(env)
    if len(args_node) == 0 or len(args_node) == 1:
        raise RuntimeError('strget is not call with two arguments')
    str = args_node[0].interpret(env)
    char_index = args_node[1].interpret(env)
    if char_index < 0 or char_index >= len(str):
        raise RuntimeError('StrGet: incorrect char index')
    return ord(str[char_index])


def strsub(env, node):
    args_node = node.args.interpret(env)
    if len(args_node) == 0 or len(args_node) == 1 or len(args_node) == 2:
        raise RuntimeError('strsub is not call with three arguments')
    str = args_node[0].interpret(env)
    char_index_start = args_node[1].interpret(env)
    substring_length = args_node[2].interpret(env)
    if char_index_start < 0 or char_index_start >= len(str):
        raise RuntimeError('strsub: incorrect start index')
    if char_index_start + substring_length >= len(str):
        raise RuntimeError('strsub: incorrect length substring')
    return str[char_index_start:char_index_start + substring_length]


def strdup(env, node):
    args_node = node.args.interpret(env)
    if len(args_node) == 0:
        raise RuntimeError('strdup call without arguments')
    str = args_node[0].interpret(env)
    return str


def strcat(env, node):
    args_node = node.args.interpret(env)
    if len(args_node) == 0 or len(args_node) == 1:
        raise RuntimeError('strcat is not call with two arguments')
    str1 = args_node[0].interpret(env)
    str2 = args_node[1].interpret(env)
    return str1 + str2


def strcmp(env, node):
    args_node = node.args.interpret(env)
    if len(args_node) == 0 or len(args_node) == 1:
        raise RuntimeError('strcmp is not call with two arguments')
    str1 = args_node[0].interpret(env)
    str2 = args_node[1].interpret(env)
    str1_list = list(str1)
    str2_list = list(str2)
    char_counter = 0
    for char in str1_list:
        if char > str2_list[char_counter]:
            return 1
        elif char < str2_list[char_counter]:
            return -1
        char_counter += 1
    if len(str1) == len(str2):
        return 0
    else:
        return 1  # str1 is a substring of str2 (str2 is greater than str1)


def strmake(env, node):
    args_node = node.args.interpret(env)
    if len(args_node) == 0 or len(args_node) == 1:
        raise RuntimeError('strmake is not call with two arguments')
    repeat_count = args_node[0].interpret(env)
    char = args_node[1].interpret(env)
    return chr(char) * repeat_count
