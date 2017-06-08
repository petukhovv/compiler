from Helpers.environment import *

def char(env, character):
    return ord(character)

def string(env, characters):
    return characters

def str_len(env, args):
    args_node = args.eval()
    if len(args_node) == 0:
        raise RuntimeError('strlen call without arguments')
    str = args_node[0].eval(env)
    return len(str)

def str_get(env, args):
    args_node = args.eval()
    if len(args_node) == 0 or len(args_node) == 1:
        raise RuntimeError('strget is not call with two arguments')
    str = args_node[0].eval(env)
    char_index = args_node[1].eval(env)
    if char_index < 0 or char_index >= len(str):
        raise RuntimeError('StrGet: incorrect char index')
    return ord(str[char_index])

def str_sub(env, args):
    args_node = args.eval()
    if len(args_node) == 0 or len(args_node) == 1 or len(args_node) == 2:
        raise RuntimeError('strsub is not call with three arguments')
    str = args_node[0].eval(env)
    char_index_start = args_node[1].eval(env)
    substring_length = args_node[2].eval(env)
    if char_index_start < 0 or char_index_start >= len(str):
        raise RuntimeError('strsub: incorrect start index')
    if char_index_start + substring_length >= len(str):
        raise RuntimeError('strsub: incorrect length substring')
    return str[char_index_start:char_index_start + substring_length]

def str_dup(env, args):
    args_node = args.eval()
    if len(args_node) == 0:
        raise RuntimeError('strdup call without arguments')
    str = args_node[0].eval(env)
    return str

def str_set(env, args):
    args_node = args.eval()
    if len(args_node) == 0 or len(args_node) == 1 or len(args_node) == 2:
        raise RuntimeError('strset is not call with three arguments')
    str = args_node[0].eval(env)
    var_name = args_node[0].name
    char_index = args_node[1].eval(env)
    if char_index < 0 or char_index >= len(str):
        raise RuntimeError('strset: incorrect index')
    new_char = args_node[2].eval(env)
    new_str = list(str)
    new_str[char_index] = chr(new_char)
    Environment(env).set(var_name, "".join(new_str))

def str_cat(env, args):
    args_node = args.eval()
    if len(args_node) == 0 or len(args_node) == 1:
        raise RuntimeError('strcat is not call with two arguments')
    str1 = args_node[0].eval(env)
    str2 = args_node[1].eval(env)
    return str1 + str2

def str_cmp(env, args):
    args_node = args.eval()
    if len(args_node) == 0 or len(args_node) == 1:
        raise RuntimeError('strcmp is not call with two arguments')
    str1 = args_node[0].eval(env)
    str2 = args_node[1].eval(env)
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

def str_make(env, args):
    args_node = args.eval()
    if len(args_node) == 0 or len(args_node) == 1:
        raise RuntimeError('strmake is not call with two arguments')
    repeat_count = args_node[0].eval(env)
    char = args_node[1].eval(env)
    return chr(char) * repeat_count
