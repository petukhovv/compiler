from Helpers.string import *

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
    var_type = Environment.get_var_type(env, name)
    var_value = Environment.get_var(env, name)
    if var_type == 'String':
        String.compile_get(commands, env, var_value)
    else:
        commands.append(assemble(Load, var_value))
