from equality import *

"""
Base class for array classes.
"""
class ArrayBase(Equality):
    pass

class UnboxedArray(ArrayBase):
    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        return 'Array(%s)' % self.elements

    def eval(self, env):
        return self.elements.eval()

class ArrLen(ArrayBase):
    def __init__(self, args):
        self.args = args

    def __repr__(self):
        return 'ArrLen(%s)' % self.args

    def eval(self, env):
        args_node = self.args.eval()
        if len(args_node) == 0:
            raise RuntimeError('arrlen call without arguments')
        arr = args_node[0].eval(env)
        return len(arr)
