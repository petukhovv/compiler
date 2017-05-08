from equality import *

"""
Base class for string classes.
"""
class StringBase(Equality):
    pass

"""
'While' statement class for AST.
eval - runtime function for Evaluator (body eval while condition).
"""
class String(StringBase):
    def __init__(self, characters):
        self.characters = characters

    def __repr__(self):
        return 'String(%s)' % self.characters

    def eval(self, env):
        return self.characters

"""
'While' statement class for AST.
eval - runtime function for Evaluator (body eval while condition).
"""
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

"""
'While' statement class for AST.
eval - runtime function for Evaluator (body eval while condition).
"""
class StrGet(StringBase):
    def __init__(self, args):
        self.args = args

    def __repr__(self):
        return 'StrLen(%s)' % self.args

    def eval(self, env):
        args_node = self.args.eval()
        if len(args_node) == 0 or len(args_node) == 1:
            raise RuntimeError('StrGet is not call with two arguments')
        str = args_node[0].eval(env)
        char_index = args_node[1].eval(env)
        if char_index < 0 or char_index >= len(str):
            raise RuntimeError('StrGet: incorrect char index')
        return str[char_index]
