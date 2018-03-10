# -*- coding: utf-8 -*-

from .Deep.strings import *

""" Мапа: арифметический оператор в языке программирования - арифметический оператор в коде стековой машины """
binop_compare_map = {
    '+': Add,
    '-': Sub,
    '*': Mul,
    '/': Div,
    '%': Mod
}


def int_aexp(commands, data, i):
    """ Компиляция числа """
    commands.add(Push, i)

    return commands.set_and_return_type(Types.INT)


def binop_aexp(commands, data, op, left, right):
    """ Компиляция арифметического выражения """
    left.compile_vm(commands, data)
    commands.clean_type()
    right.compile_vm(commands, data)
    commands.clean_type()

    commands.add(binop_compare_map[op])

    return commands.set_and_return_type(Types.INT)


def var_aexp(commands, data, name, context, value_type):
    """ Компиляция переменной """
    if context == 'assign':
        var = data.var(alias=name, type=value_type, double_size=True)

        if data.defined_object is not None:
            data.set_link_object(var, data.defined_object)
            data.defined_objects = None
        commands.store_value(var, type=value_type)
    else:
        var_number = data.get_var(name)
        compile_time_type = data.get_type(var_number)
        commands.add(Load, var_number)
        if compile_time_type == Types.DYNAMIC:
            commands.add(Push, var_number)
            commands.add(BLoad, 1)
            return Types.DYNAMIC
        else:
            return commands.set_and_return_type(compile_time_type)
