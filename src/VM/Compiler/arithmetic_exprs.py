from ..commands import *
from ..Helpers.assembler import *

def binop_aexp(commands, env, op, left, right):
    left.compile_vm(commands, env)
    right.compile_vm(commands, env)
    if op == '+':
        value = assemble(Add)
    elif op == '-':
        value = assemble(Sub)
    elif op == '*':
        value = assemble(Mul)
    elif op == '/':
        value = assemble(Div)
    elif op == '%':
        value = assemble(Mod)
    else:
        raise RuntimeError('unknown operator: ' + op)
    commands.append(value)

def int_aexp(commands, env, i):
    commands.append(assemble(Push, i))

def var_aexp(commands, env, name):
    commands.append(assemble(Load, env['vars_map'][name]))
