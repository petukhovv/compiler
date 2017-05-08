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
        return 'UnboxedArray(%s)' % self.elements

    def eval(self, env):
        return self.elements.eval()

class ArrayElement(ArrayBase):
    def __init__(self, array, index):
        self.array = array
        self.index = index

    def __repr__(self):
        return 'ArrayElement(%s, %s)' % (self.array, self.index)

    def eval(self, env):
        arr = env['v'][self.array]
        index = self.index.eval(env)
        if index >= len(arr):
            raise RuntimeError('Array index out of range')
        return arr[index]

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

class UnboxedArrMake(ArrayBase):
    def __init__(self, args):
        self.args = args

    def __repr__(self):
        return 'UnboxedArrMake(%s)' % self.args

    def eval(self, env):
        arr = []
        index = 0
        args = self.args.eval()
        count = args[0].eval(env)
        if len(args) == 2:
            default_value = args[1].eval(env)
        else:
            default_value = 0
        while index < count:
            arr.append(default_value)
            index += 1
        return arr
