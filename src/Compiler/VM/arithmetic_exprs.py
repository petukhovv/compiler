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
def var_aexp(commands, data, name):
    var_number = data.get_var(name)

    commands.add(Load, var_number)

    return commands.set_and_return_type(data.get_type(var_number))
