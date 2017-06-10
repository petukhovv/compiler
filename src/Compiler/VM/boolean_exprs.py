from src.VM.commands import *
from src.VM.Helpers.assembler import *

def relop_bexp(commands, env, op, left, right):
    left.compile_vm(commands, env)
    right.compile_vm(commands, env)
    if op == '==':
        value = assemble(Compare, 0)
    elif op == '!=':
        value = assemble(Compare, 1)
    elif op == '<':
        value = assemble(Compare, 2)
    elif op == '>':
        value = assemble(Compare, 3)
    elif op == '<=':
        value = assemble(Compare, 4)
    elif op == '>=':
        value = assemble(Compare, 5)
    else:
        raise RuntimeError('unknown operator: ' + op)
    commands.append(value)
