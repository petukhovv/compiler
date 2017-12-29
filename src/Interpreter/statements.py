from Parser.AST.common import *
from Parser.AST.arrays import *

from .Helpers.environment import *
from .Helpers.common import BoxedArrayWrap, UnboxedArrayWrap


def assign_statement(env, variable, aexp):
    """
    Assign statement def for AST.
    eval - runtime function for Evaluator (return variable by name from environment).
    Example: x := 56
    """
    value = aexp.eval(env)
    if isinstance(variable, ArrayElement):
        arr_descr = variable
        index = arr_descr.index.eval(env)
        arr = Environment(env).get(arr_descr.array)
        value_is_array = isinstance(aexp, UnboxedArrayWrap) or isinstance(aexp, BoxedArrayWrap)
        array_is_unboxed = isinstance(arr, UnboxedArrayWrap)
        if value_is_array or array_is_unboxed:
            arr[index] = value
        else:
            arr[index] = Pointer(env, aexp)
        Environment(env).set(arr_descr.array, arr)
    else:
        name = variable.name
        Environment(env).set(name, value)


def compound_statement(env, first, second):
    """
    Compound statement def for AST.
    eval - runtime function for Evaluator (eval first and second statement operators).
    """
    first.eval(env)
    second.eval(env)


def if_statement(env, condition, true_stmt, alternatives_stmt, false_stmt):
    """
    'If' statement def for AST.
    eval - runtime function for Evaluator (true of false statement depending on condition).
    """
    condition_value = condition.eval(env)
    if condition_value:
        true_stmt.eval(env)
    else:
        if alternatives_stmt:
            for alternative_stmt in alternatives_stmt:
                alternative_condition_value = alternative_stmt.eval(env)
                if alternative_condition_value:
                    return True
        if false_stmt:
            false_stmt.eval(env)
    return condition_value


def while_statement(env, condition, body):
    """
    'While' statement def for AST.
    eval - runtime function for Evaluator (body eval while condition).
    """
    while condition.eval(env):
        body.eval(env)


def for_statement(env, stmt1, stmt2, stmt3, body):
    """
    'For' statement def for AST.
    eval - runtime function for Evaluator ('for' loop).
    """
    stmt1.eval(env)
    while stmt2.eval(env):
        iteration_env = Environment(env).create()
        body.eval(iteration_env)
        stmt3.eval(env)
    return


def repeat_statement(env, condition, body):
    """
    'Repeat' statement def for AST.
    eval - runtime function for Evaluator (body eval while condition).
    """
    while True:
        body.eval(env)
        condition_value = condition.eval(env)
        if condition_value:
            break


def skip_statement(env):
    """
    'Skip' statement def for AST.
    eval - runtime function for Evaluator (empty function).
    """
    pass
