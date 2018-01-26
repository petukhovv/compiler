import sys

from Parser.AST.common import *

arrays = sys.modules['Parser.AST.arrays']

from .Helpers.environment import *
from .Helpers.common import __fill_array, BoxedArrayWrap, UnboxedArrayWrap


def unboxed_array(env, elements):
    return elements.interpret()


def boxed_array(env, elements):
    return elements.interpret()


def array_element(env, array, index, other_indexes):
    arr = Environment(env).get(array)
    index = index.interpret(env)
    if index >= len(arr):
        raise RuntimeError('Array index out of range')
    element = arr[index]
    # TODO: run [] operators independently (Arr[]...[]..., not Arr[][])
    if other_indexes:
        if isinstance(element, Pointer):
            element = element.interpret()
        if not isinstance(element, list):
            raise RuntimeError('Array element is not array')
        for other_index in other_indexes:
            other_index_number = other_index.interpret(env)
            if other_index_number >= len(element):
                raise RuntimeError('Array index out of range')
            if isinstance(element, Pointer):
                element = element.interpret()
            if not isinstance(element, list):
                raise RuntimeError('Array element is not array')
            element = element[other_index_number]
    if isinstance(element, Pointer):
        return element.interpret()
    else:
        return element


def arr_len(env, args):
    args_node = args.interpret()
    if len(args_node) == 0:
        raise RuntimeError('arrlen call without arguments')
    arr = args_node[0].interpret(env)
    return len(arr)


def unboxed_arr_make(env, args):
    arr = []
    args = args.interpret()
    count = args[0].interpret(env)
    if len(args) == 2:
        default_value_is_array = isinstance(args[1], arrays.UnboxedArray)
        default_value = args[1].interpret(env)
    else:
        default_value_is_array = False
        default_value = 0
    if default_value_is_array:
        if len(default_value) == 0:
            arr = __fill_array(arr, count, 0)
        elif len(default_value) != count:
            raise RuntimeError('Length default array is not the same length as the specified.')
        else:
            arr = default_value
    else:
        arr = __fill_array(arr, count, default_value)
    arr = UnboxedArrayWrap(arr)
    return arr


def boxed_arr_make(env, args):
    arr = []
    args = args.interpret()
    count = args[0].interpret(env)
    if len(args) == 2:
        default_value_is_array = isinstance(args[1], arrays.BoxedArray)
        if default_value_is_array:
            default_value = args[1].interpret(env)
        else:
            default_value = args[1]
    else:
        default_value_is_array = False
        default_value = arrays.IntAexp(0)
    if default_value_is_array:
        if len(default_value) == 0:
            arr = __fill_array(arr, count, arrays.BoxedArray(Enumeration([])))
        elif len(default_value) != count:
            raise RuntimeError('Length default array is not the same length as the specified.')
        else:
            arr = default_value
    else:
        arr = __fill_array(arr, count, default_value)
    arr = BoxedArrayWrap(arr)
    return arr
