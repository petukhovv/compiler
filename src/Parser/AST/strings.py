from equality import *

"""
Base class for string classes.
"""
class StringBase(Equality):
    pass

class String(StringBase):
    def __init__(self, characters):
        self.characters = characters

    def __repr__(self):
        return 'String(%s)' % self.characters

    def eval(self, env):
        return self.characters

class StrLen(StringBase):
    def __init__(self, args):
        self.args = args

    def __repr__(self):
        return 'StrLen(%s)' % self.args

    def eval(self, env):
        args_node = self.args.eval()
        if len(args_node) == 0:
            raise RuntimeError('Strlen call without arguments')
        str = args_node[0].eval(env)
        return len(str)

class StrGet(StringBase):
    def __init__(self, args):
        self.args = args

    def __repr__(self):
        return 'StrGet(%s)' % self.args

    def eval(self, env):
        args_node = self.args.eval()
        if len(args_node) == 0 or len(args_node) == 1:
            raise RuntimeError('StrGet is not call with two arguments')
        str = args_node[0].eval(env)
        char_index = args_node[1].eval(env)
        if char_index < 0 or char_index >= len(str):
            raise RuntimeError('StrGet: incorrect char index')
        return str[char_index]

class StrSub(StringBase):
    def __init__(self, args):
        self.args = args

    def __repr__(self):
        return 'StrSub(%s)' % self.args

    def eval(self, env):
        args_node = self.args.eval()
        if len(args_node) == 0 or len(args_node) == 1 or len(args_node) == 2:
            raise RuntimeError('StrSub is not call with three arguments')
        str = args_node[0].eval(env)
        char_index_start = args_node[1].eval(env)
        substring_length = args_node[2].eval(env)
        if char_index_start < 0 or char_index_start >= len(str):
            raise RuntimeError('StrGet: incorrect start index')
        if char_index_start + substring_length >= len(str):
            raise RuntimeError('StrGet: incorrect length substring')
        return str[char_index_start:char_index_start + substring_length]
