from src.Parser.AST.common import *
from src.Parser.AST.arithmetic_exprs import *

class UnboxedArrayWrap(list): pass

class BoxedArrayWrap(list): pass

def fill_array(arr, count, default_value):
    index = 0
    while index < count:
        arr.append(default_value)
        index += 1
    return arr

class UnboxedArray:
    pointers = 0

    def __init__(self, elements):
        self.elements = elements

    def eval(self, env):
        return self.elements.eval()

class BoxedArray:
    pointers = 0

    def __init__(self, elements):
        self.elements = elements

    def eval(self, env):
        return self.elements.eval()

class ArrayElement:
    pointers = 0

    def __init__(self, array, index, other_indexes=None):
        self.array = array
        self.index = index
        self.other_indexes = other_indexes

    def eval(self, env):
        arr = Environment(env).get(self.array)
        index = self.index.eval(env)
        if index >= len(arr):
            raise RuntimeError('Array index out of range')
        element = arr[index]
        # TODO: interpret [] operators independently (Arr[]...[]..., not Arr[][])
        if self.other_indexes:
            if isinstance(element, Pointer):
                element = element.eval()
            if not isinstance(element, list):
                raise RuntimeError('Array element is not array')
            for other_index in self.other_indexes:
                if other_index >= len(element):
                    raise RuntimeError('Array index out of range')
                if isinstance(element, Pointer):
                    element = element.eval()
                if not isinstance(element, list):
                    raise RuntimeError('Array element is not array')
                element = element[other_index.eval(env)]
        if isinstance(element, Pointer):
            return element.eval()
        else:
            return element

class ArrLen:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        args_node = self.args.eval()
        if len(args_node) == 0:
            raise RuntimeError('arrlen call without arguments')
        arr = args_node[0].eval(env)
        return len(arr)

class UnboxedArrMake:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        arr = []
        args = self.args.eval()
        count = args[0].eval(env)
        if len(args) == 2:
            default_value_is_array = isinstance(args[1], UnboxedArray)
            default_value = args[1].eval(env)
        else:
            default_value_is_array = False
            default_value = 0
        if default_value_is_array:
            if len(default_value) == 0:
                arr = fill_array(arr, count, 0)
            elif len(default_value) != count:
                raise RuntimeError('Length default array is not the same length as the specified.')
            else:
                arr = default_value
        else:
            arr = fill_array(arr, count, default_value)
        arr = UnboxedArrayWrap(arr)
        return arr

class BoxedArrMake:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        arr = []
        args = self.args.eval()
        count = args[0].eval(env)
        if len(args) == 2:
            default_value_is_array = isinstance(args[1], BoxedArray)
            if default_value_is_array:
                default_value = args[1].eval(env)
            else:
                default_value = args[1]
        else:
            default_value_is_array = False
            default_value = IntAexp(0)
        if default_value_is_array:
            if len(default_value) == 0:
                arr = fill_array(arr, count, BoxedArray(Enumeration([])))
            elif len(default_value) != count:
                raise RuntimeError('Length default array is not the same length as the specified.')
            else:
                arr = default_value
        else:
            arr = fill_array(arr, count, default_value)
        arr = BoxedArrayWrap(arr)
        return arr

pointer_supported_types = [UnboxedArray, BoxedArray, ArrayElement, VarAexp]
