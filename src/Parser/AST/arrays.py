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

class BoxedArray(ArrayBase):
    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        return 'BoxedArray(%s)' % self.elements

    def eval(self, env):
        return self.elements.eval()

class ArrayElement(ArrayBase):
    def __init__(self, array, index, other_indexes=None):
        self.array = array
        self.index = index
        self.other_indexes = other_indexes

    def __repr__(self):
        return 'ArrayElement(%s, %s)' % (self.array, self.index)

    def eval(self, env):
        arr = env['v'][self.array]
        index = self.index.eval(env)
        if index >= len(arr):
            raise RuntimeError('Array index out of range')
        element = arr[index]
        if self.other_indexes:
            if type(element) is not list:
                raise RuntimeError('Array element is not array')
            for other_index in self.other_indexes:
                if other_index >= len(element):
                    raise RuntimeError('Array index out of range')
                element = element[other_index.eval(env)]
        return element

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
            default_value_is_array = isinstance(args[1], UnboxedArray)
            default_value = args[1].eval(env)
        else:
            default_value_is_array = False
            default_value = 0
        if default_value_is_array:
            if len(default_value) != count:
                raise RuntimeError('Length default array is not the same length as the specified.')
            arr = default_value
        else:
            while index < count:
                arr.append(default_value)
                index += 1
        return arr

class BoxedArrMake(ArrayBase):
    def __init__(self, args):
        self.args = args

    def __repr__(self):
        return 'BoxedArrMake(%s)' % self.args

    def eval(self, env):
        arr = []
        index = 0
        args = self.args.eval()
        count = args[0].eval(env)
        if len(args) == 2:
            default_value_is_array = isinstance(args[1], BoxedArray)
            default_value = args[1].eval(env)
        else:
            default_value_is_array = False
            default_value = 0
        if default_value_is_array:
            if len(default_value) != count:
                raise RuntimeError('Length default array is not the same length as the specified.')
            arr = default_value
        else:
            while index < count:
                arr.append(default_value)
                index += 1
        return arr