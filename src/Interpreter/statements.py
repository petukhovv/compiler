from src.Parser.AST.common import *
from src.Parser.AST.arrays import *

from Helpers.environment import *
from Helpers.common import BoxedArrayWrap, UnboxedArrayWrap

"""
Assign statement def for AST.
eval - runtime function for Evaluator (return variable by name from environment).
Example: x := 56
"""
def assign_statement(env, variable, aexp):
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

"""
Compound statement def for AST.
eval - runtime function for Evaluator (eval first and second statement operators).
"""
def compound_statement(env, first, second):
    first.eval(env)
    second.eval(env)

"""
'If' statement def for AST.
eval - runtime function for Evaluator (true of false statement depending on condition).
"""
def if_statement(env, condition, true_stmt, alternatives_stmt, false_stmt):
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

"""
'While' statement def for AST.
eval - runtime function for Evaluator (body eval while condition).
"""
def while_statement(env, condition, body):
    while condition.eval(env):
        body.eval(env)

"""
'For' statement def for AST.
eval - runtime function for Evaluator ('for' loop).
"""
def for_statement(env, stmt1, stmt2, stmt3, body):
    stmt1.eval(env)
    while stmt2.eval(env):
        iteration_env = Environment(env).create()
        body.eval(iteration_env)
        stmt3.eval(env)
    return

"""
'Repeat' statement def for AST.
eval - runtime function for Evaluator (body eval while condition).
"""
def repeat_statement(env, condition, body):
    while True:
        body.eval(env)
        condition_value = condition.eval(env)
        if condition_value:
            break

"""
'Skip' statement def for AST.
eval - runtime function for Evaluator (empty function).
"""
def skip_statement(env): pass
