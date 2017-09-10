# -*- coding: utf-8 -*-

from src.Compiler.VM.Deep.arrays import *

""" Компиляция built-in функции arrmake для создания unboxed-массивов """
def unboxed_arrmake(commands, data, args):
    # Если были переданы default values (2-м аргументом), смотрим, в каком именно формате
    if len(args.elements) == 2:
        default_value_type = args_compile(args, 1, commands, data)
        commands.extract_value()
        # Если вторым аргументом был передан [], то дублируемым элементом будет 0 ( сигнатура: arrmake(n, []) )
        if default_value_type == types.UNBOXED_ARR and len(args.elements[1].elements.elements) == 0:
            commands.add(Push, 0)
            values_type = 'zeros'
        # Если [n1, n2, ...], то будем записывать в элементы заданные значения
        elif default_value_type == types.UNBOXED_ARR and len(args.elements[1].elements.elements) != 0:
            values_type = 'preset'
        # Если был передан не массив, а число, то оно и будет дублируемым элементом
        else:
            values_type = 'repeated'
    # Если ничего не было передано, то элементы массива будет пустыми (None)
    else:
        values_type = 'none'

    args_compile(args, 0, commands, data)
    commands.extract_value()
    ArrayCompiler.unboxed_arrmake(commands, data, values_type)

    return commands.set_and_return_type(types.UNBOXED_ARR)

""" Компиляция конструкции константного задания unboxed-массива: [n1, n2, ...]  """
def unboxed(commands, data, elements):
    arr_elements = elements.compile_vm(commands, data)
    commands.extract_value()
    for element in reversed(arr_elements):
        commands.add(Push, element)

    return commands.set_and_return_type(types.UNBOXED_ARR)

""" Компиляция оператора получения элемента массива: A[n] """
def array_element(commands, data, array, index, other_indexes, context):
    index.compile_vm(commands, data)
    commands.extract_value()
    commands.load_value(data.get_var(array))
    commands.extract_value()
    if context == 'assign':
        ArrayCompiler.set_element(commands, data)
    else:
        ArrayCompiler.get_element(commands, data)
        return commands.set_and_return_type(types.INT)

""" Компиляция built-in функции arrlen для получения длины массива """
def arrlen(commands, data, args):
    args_compile(args, 0, commands, data)
    commands.extract_value()
    ArrayCompiler.arrlen(commands, data)

    return commands.set_and_return_type(types.INT)
