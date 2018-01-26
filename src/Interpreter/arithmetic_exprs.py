from .Helpers.environment import *


def int_aexp(env, i):
    return i


def var_aexp(env, name):
    return Environment(env).get(name)


def binop_aexp(env, op, left, right):
    left_value = left.interpret(env)
    right_value = right.interpret(env)
    if op == '+':
        value = left_value + right_value
    elif op == '-':
        value = left_value - right_value
    elif op == '*':
        value = left_value * right_value
    elif op == '/':
        value = int(left_value / right_value)
    elif op == '%':
        value = left_value % right_value
        if left_value < 0 and value != 0 and right_value > 0:
            value -= right_value
        elif right_value < 0 and value != 0 and left_value > 0:
            value -= right_value
    else:
        raise RuntimeError('unknown operator: ' + op)
    return value
