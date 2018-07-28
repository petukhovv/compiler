from .Helpers.environment import *


def int_aexp(env, node):
    return node.i


def var_aexp(env, node):
    return Environment(env).get(node.name)


def binop_aexp(env, node):
    left_value = node.left.interpret(env)
    right_value = node.right.interpret(env)
    if node.op == '+':
        value = left_value + right_value
    elif node.op == '-':
        value = left_value - right_value
    elif node.op == '*':
        value = left_value * right_value
    elif node.op == '/':
        value = int(left_value / right_value)
    elif node.op == '%':
        value = left_value % right_value
        if left_value < 0 and value != 0 and right_value > 0:
            value -= right_value
        elif right_value < 0 and value != 0 and left_value > 0:
            value -= right_value
    else:
        raise RuntimeError('unknown operator: ' + op)
    return value
