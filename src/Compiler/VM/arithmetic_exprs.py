from src.VM.commands import *
from src.VM.Helpers.assembler import *
from pprint import pprint
from Helpers.environment import *

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
    commands.append(assemble(Load, Environment.get_var(env, name)))
