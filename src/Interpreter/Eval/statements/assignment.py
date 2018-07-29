from Parser.AST.common import Pointer
from Parser.AST.expressions.arrays import ArrayElement
from Parser.AST.expressions.objects import ObjectVal
from Parser.AST.declarations.object import Object

from ...Helpers.environment import Environment
from ...Helpers.common import BoxedArrayWrap, UnboxedArrayWrap


def assign_statement(env, node):
    """
    Assign statement def for AST.
    interpret - runtime function for Evaluator (return variable by name from environment).
    Example: x := 56
    """
    value = node.aexp.interpret(env)
    if isinstance(node.variable, ArrayElement):
        arr_descr = node.variable
        index = arr_descr.index.interpret(env)
        arr = Environment(env).get(arr_descr.array)
        value_is_array = isinstance(node.aexp, UnboxedArrayWrap) or isinstance(node.aexp, BoxedArrayWrap)
        array_is_unboxed = isinstance(arr, UnboxedArrayWrap)
        if value_is_array or array_is_unboxed:
            arr[index] = value
        else:
            arr[index] = Pointer(env, node.aexp)
        Environment(env).set(arr_descr.array, arr)
    elif isinstance(node.variable, ObjectVal):
        obj_descr = node.variable
        prop_name = obj_descr.prop_name

        if obj_descr.object_name == 'this':
            obj = Environment.context_objects[-1]
        else:
            obj = Environment(env).get(obj_descr.object_name)
        value_is_reference = isinstance(node.aexp, UnboxedArrayWrap) or isinstance(node.aexp, BoxedArrayWrap) or isinstance(node.aexp, Object)
        if not value_is_reference:
            obj.set(prop_name, value)
        else:
            obj.set(prop_name, Pointer(env, node.aexp))
        Environment(env).set(obj_descr.object_name, obj)
    else:
        name = node.variable.name
        Environment(env).set(name, value)

