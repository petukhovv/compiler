from Parser.AST.common import *
from Parser.AST.arrays import *
from Parser.AST.objects import *

from .Helpers.environment import *
from .Helpers.common import BoxedArrayWrap, UnboxedArrayWrap


def assign_statement(env, variable, aexp):
    """
    Assign statement def for AST.
    interpret - runtime function for Evaluator (return variable by name from environment).
    Example: x := 56
    """
    value = aexp.interpret(env)
    if isinstance(variable, ArrayElement):
        arr_descr = variable
        index = arr_descr.index.interpret(env)
        arr = Environment(env).get(arr_descr.array)
        value_is_array = isinstance(aexp, UnboxedArrayWrap) or isinstance(aexp, BoxedArrayWrap)
        array_is_unboxed = isinstance(arr, UnboxedArrayWrap)
        if value_is_array or array_is_unboxed:
            arr[index] = value
        else:
            arr[index] = Pointer(env, aexp)
        Environment(env).set(arr_descr.array, arr)
    elif isinstance(variable, ObjectVal):
        obj_descr = variable
        prop_name = obj_descr.prop_name
        obj = Environment(env).get(obj_descr.object_name)
        value_is_reference = isinstance(aexp, UnboxedArrayWrap) or isinstance(aexp, BoxedArrayWrap) or isinstance(aexp, Object)
        if not value_is_reference:
            obj.set(prop_name, value)
        else:
            obj.set(prop_name, Pointer(env, aexp))
        Environment(env).set(obj_descr.object_name, obj)
    else:
        name = variable.name
        Environment(env).set(name, value)


def compound_statement(env, first, second):
    """
    Compound statement def for AST.
    interpret - runtime function for Evaluator (interpret first and second statement operators).
    """
    first.interpret(env)
    second.interpret(env)


def if_statement(env, condition, true_stmt, alternatives_stmt, false_stmt):
    """
    'If' statement def for AST.
    interpret - runtime function for Evaluator (true of false statement depending on condition).
    """
    condition_value = condition.interpret(env)
    if condition_value:
        true_stmt.interpret(env)
    else:
        if alternatives_stmt:
            for alternative_stmt in alternatives_stmt:
                alternative_condition_value = alternative_stmt.interpret(env)
                if alternative_condition_value:
                    return True
        if false_stmt:
            false_stmt.interpret(env)
    return condition_value


def while_statement(env, condition, body):
    """
    'While' statement def for AST.
    interpret - runtime function for Evaluator (body interpret while condition).
    """
    while condition.interpret(env):
        body.interpret(env)


def for_statement(env, stmt1, stmt2, stmt3, body):
    """
    'For' statement def for AST.
    interpret - runtime function for Evaluator ('for' loop).
    """
    stmt1.interpret(env)
    while stmt2.interpret(env):
        iteration_env = Environment(env).create()
        body.interpret(iteration_env)
        stmt3.interpret(env)
    return


def repeat_statement(env, condition, body):
    """
    'Repeat' statement def for AST.
    interpret - runtime function for Evaluator (body interpret while condition).
    """
    while True:
        body.interpret(env)
        condition_value = condition.interpret(env)
        if condition_value:
            break


def skip_statement(env):
    """
    'Skip' statement def for AST.
    interpret - runtime function for Evaluator (empty function).
    """
    pass
