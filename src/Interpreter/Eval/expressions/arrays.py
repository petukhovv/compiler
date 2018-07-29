from Parser.AST.common import Pointer, Enumeration

from ...Helpers.environment import Environment
from ...Helpers.types import Types
from ...Helpers.common import __fill_array, BoxedArrayWrap, UnboxedArrayWrap


def arrmake_inline(env, node):
    return node.elements.interpret(env)


def array_element(env, node):
    arr = Environment(env).get(node.array)
    index = node.index.interpret(env)
    if index >= len(arr):
        raise RuntimeError('Array index out of range')
    element = arr[index]
    # TODO: run [] operators independently (Arr[]...[]..., not Arr[][])
    if node.other_indexes:
        if isinstance(element, Pointer):
            element = element.interpret(env)
        if not isinstance(element, list):
            raise RuntimeError('Array element is not array')
        for other_index in node.other_indexes:
            other_index_number = other_index.interpret(env)
            if other_index_number >= len(element):
                raise RuntimeError('Array index out of range')
            if isinstance(element, Pointer):
                element = element.interpret(env)
            if not isinstance(element, list):
                raise RuntimeError('Array element is not array')
            element = element[other_index_number]
    if isinstance(element, Pointer):
        return element.interpret(env)
    else:
        return element


def arrlen(env, node):
    args_node = node.args.interpret(env)
    if len(args_node) == 0:
        raise RuntimeError('arrlen call without arguments')
    arr = args_node[0].interpret(env)
    return len(arr)


def arrmake(env, node):
    from Parser.AST.expressions.arrays import BoxedArray, UnboxedArray
    from Parser.AST.expressions.arithmetic import IntAexp

    type = Types.BOXED_ARR if node.type == 'boxed' else Types.UNBOXED_ARR

    arr = []
    args = node.args.interpret(env)
    count = args[0].interpret(env)
    if len(args) == 2:
        default_value_is_array = isinstance(args[1], UnboxedArray if type == Types.UNBOXED_ARR else BoxedArray)
        if default_value_is_array or type == Types.UNBOXED_ARR:
            default_value = args[1].interpret(env)
        else:
            default_value = args[1]
    else:
        default_value_is_array = False
        default_value = 0 if type == Types.UNBOXED_ARR else IntAexp(0)
    if default_value_is_array:
        if len(default_value) == 0:
            arr = __fill_array(arr, count, 0 if type == Types.UNBOXED_ARR else BoxedArray(Enumeration([])))
        elif len(default_value) != count:
            raise RuntimeError('Length default array is not the same length as the specified.')
        else:
            arr = default_value
    else:
        arr = __fill_array(arr, count, default_value)

    return UnboxedArrayWrap(arr) if type == Types.UNBOXED_ARR else BoxedArrayWrap(arr)
