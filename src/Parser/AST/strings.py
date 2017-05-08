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
    def __init__(self, characters):
        self.characters = characters

    def __repr__(self):
        return 'String(%s)' % self.characters

    def eval(self, env):
        return self.characters
