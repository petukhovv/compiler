from pprint import pprint
from Helpers.environment import *

def int_aexp(env, i):
    return i

def var_aexp(env, name):
    return Environment(env).get(name)

def binop_aexp(env, op, left, right):
    left_value = left.eval(env)
    right_value = right.eval(env)
    if op == '+':
        value = left_value + right_value
    elif op == '-':
        value = left_value - right_value
    elif op == '*':
        value = left_value * right_value
    elif op == '/':
        value = left_value / right_value
    elif op == '%':
        value = left_value % right_value
    else:
        raise RuntimeError('unknown operator: ' + op)
    return value
