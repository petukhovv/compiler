from Helpers.string import *
from Helpers.assembler import Commands

def binop_aexp(commands, env, op, left, right):
    left.compile_vm(commands, env)
    right.compile_vm(commands, env)
    if op == '+':
        value = Commands.gen(Add)
    elif op == '-':
        value = Commands.gen(Sub)
    elif op == '*':
        value = Commands.gen(Mul)
    elif op == '/':
        value = Commands.gen(Div)
    elif op == '%':
        value = Commands.gen(Mod)
    else:
        raise RuntimeError('unknown operator: ' + op)
    commands.append(value)

def int_aexp(commands, env, i):
    commands.add(Push, i)

def var_aexp(commands, env, name):
    var_type = Environment.get_var_type(env, name)
    var_value = Environment.get_var(env, name)
    if var_type == 'String':
        String.compile_load(commands, env, var_value)
    else:
        commands.add(Load, var_value)
