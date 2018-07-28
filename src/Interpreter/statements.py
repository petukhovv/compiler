from Parser.AST.common import *
from Parser.AST.arrays import *
from Parser.AST.objects import *

from .Helpers.environment import *
from .Helpers.common import BoxedArrayWrap, UnboxedArrayWrap


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


def compound_statement(env, node):
    """
    Compound statement def for AST.
    interpret - runtime function for Evaluator (interpret first and second statement operators).
    """
    node.first.interpret(env)
    node.second.interpret(env)


def if_statement(env, node):
    """
    'If' statement def for AST.
    interpret - runtime function for Evaluator (true of false statement depending on condition).
    """
    condition_value = node.condition.interpret(env)
    if condition_value:
        node.true_stmt.interpret(env)
    else:
        if node.alternatives_stmt:
            for alternative_stmt in node.alternatives_stmt:
                alternative_condition_value = alternative_stmt.interpret(env)
                if alternative_condition_value:
                    return True
        if node.false_stmt:
            node.false_stmt.interpret(env)
    return condition_value


def while_statement(env, node):
    """
    'While' statement def for AST.
    interpret - runtime function for Evaluator (body interpret while condition).
    """
    while node.condition.interpret(env):
        node.body.interpret(env)


def for_statement(env, node):
    """
    'For' statement def for AST.
    interpret - runtime function for Evaluator ('for' loop).
    """
    node.stmt1.interpret(env)
    while node.stmt2.interpret(env):
        iteration_env = Environment(env).create()
        node.body.interpret(iteration_env)
        node.stmt3.interpret(env)
    return


def repeat_statement(env, node):
    """
    'Repeat' statement def for AST.
    interpret - runtime function for Evaluator (body interpret while condition).
    """
    while True:
        node.body.interpret(env)
        condition_value = node.condition.interpret(env)
        if condition_value:
            break


def skip_statement(env, node):
    """
    'Skip' statement def for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    pass
