# -*- coding: utf-8 -*-

from ...Helpers.commands import Add, Sub, Mul, Div, Mod, Push, Load, BLoad
from ...Helpers.types import Types

""" Мапа: арифметический оператор в языке программирования - арифметический оператор в коде стековой машины """
binop_compare_map = {
    '+': Add,
    '-': Sub,
    '*': Mul,
    '/': Div,
    '%': Mod
}


def int_aexp(commands, data, node):
    """ Компиляция числа """
    commands.add(Push, node.i)

    return commands.set_and_return_type(Types.INT)


def binop_aexp(commands, data, node):
    """ Компиляция арифметического выражения """
    node.left.compile_vm(commands, data)
    commands.clean_type()
    node.right.compile_vm(commands, data)
    commands.clean_type()

    commands.add(binop_compare_map[node.op])

    return commands.set_and_return_type(Types.INT)


def var_aexp(commands, data, node):
    """ Компиляция переменной """
    if node.context == 'assign':
        var = data.var(alias=node.name, type=node.type, double_size=True)

        if data.defined_object is not None:
            data.set_link_object(var, data.defined_object)
            data.defined_objects = None
        commands.store_value(var, type=node.type)
    else:
        var_number = data.get_var(node.name)
        compile_time_type = data.get_type(var_number)
        commands.add(Load, var_number)
        if compile_time_type == Types.DYNAMIC:
            commands.add(Push, var_number)
            commands.add(BLoad, 1)
            return Types.DYNAMIC
        else:
            return commands.set_and_return_type(compile_time_type)
