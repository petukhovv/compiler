# -*- coding: utf-8 -*-

from src.Compiler.VM.Deep.strings import *

""" Мапа: арифметический оператор в языке программирования - арифметический оператор в коде стековой машины """
binop_compare_map = {
    '+': Add,
    '-': Sub,
    '*': Mul,
    '/': Div,
    '%': Mod
}

""" Компиляция арифметического выражения """
def binop_aexp(commands, data, op, left, right):
    left.compile_vm(commands, data)
    commands.extract_value()
    right.compile_vm(commands, data)
    commands.extract_value()

    commands.add(binop_compare_map[op])

    return commands.set_and_return_type(types.INT)

""" Компиляция числа """
def int_aexp(commands, data, i):
    commands.add(Push, i)

    return commands.set_and_return_type(types.INT)

""" Компиляция переменной """
def var_aexp(commands, data, name, context, value_type):
    if context == 'assign':
        commands.store_value(data.var(alias=name, type=value_type, double_size=True), type=value_type)
    else:
        var_number = data.get_var(name)
        compile_time_type = data.get_type(var_number)
        commands.add(Load, var_number)
        if compile_time_type == types.DYNAMIC:
            commands.add(Push, var_number)
            commands.add(BLoad, 1)
            return types.DYNAMIC
        else:
            return commands.set_and_return_type(compile_time_type)
