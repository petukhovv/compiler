# -*- coding: utf-8 -*-

from Deep.arrays import *

""" Компиляция built-in функции arrmake для создания unboxed-массивов """
def arrmake(commands, data, args, type):
    type = Types.BOXED_ARR if type == 'boxed' else Types.UNBOXED_ARR

    # Если были переданы default values (2-м аргументом), смотрим, в каком именно формате
    if len(args.elements) == 2:
        default_value_type = args.elements[1].compile_vm(commands, data)
        commands.extract_value()
        # Если вторым аргументом был передан [], то дублируемым элементом будет 0 ( сигнатура: arrmake(n, []) )
        if default_value_type == type and len(args.elements[1].elements.elements) == 0:
            commands.add(Pop)
            commands.add(Push, 0)
            values_type = 'zeros'
        # Если [n1, n2, ...], то будем записывать в элементы заданные значения
        elif default_value_type == type and len(args.elements[1].elements.elements) != 0:
            return commands.set_and_return_type(type)
        # Если был передан не массив, а число, то оно и будет дублируемым элементом
        else:
            values_type = 'repeated'
    # Если ничего не было передано, то элементы массива будет пустыми (None)
    else:
        values_type = 'none'

    args_compile(args, 0, commands, data)
    commands.extract_value()
    ArrayCompiler.arrmake(commands, data, values_type)

    return commands.set_and_return_type(type)

""" Компиляция конструкции константного задания unboxed-массива: [n1, n2, ...]  """
def arrmake_inline(commands, data, elements, type):
    type = Types.BOXED_ARR if type == 'boxed' else Types.UNBOXED_ARR

    arr_elements = elements.compile_vm(commands, data)

    arrlen_var = data.var()
    commands.add(Push, len(arr_elements))
    commands.add(Store, arrlen_var)

    for element in reversed(arr_elements):
        if type == Types.BOXED_ARR:
            element = data.get_var(element)
            element_type = data.get_type(element)
            commands.add(Load, element)
        else:
            element_type = Types.DYNAMIC
            commands.add(Push, element)
        commands.add(Push, element_type)

    commands.add(Load, arrlen_var)

    ArrayCompiler.arrmake(commands, data, 'preset')

    return commands.set_and_return_type(type)

""" Компиляция оператора получения элемента массива: A[n] """
def array_element(commands, data, array, index, other_indexes, context):
    var_number = data.get_var(array)
    var_type = data.get_type(var_number)
    commands.load_value(var_number)
    commands.extract_value()

    index.compile_vm(commands, data)
    commands.extract_value()
    if context == 'assign':
        if other_indexes is not None:
            for other_index in other_indexes:
                ArrayCompiler.get_element(commands, data, var_type)
                commands.extract_value()
                other_index.compile_vm(commands, data)
                commands.extract_value()
        ArrayCompiler.set_element(commands, data, var_type)
    else:
        ArrayCompiler.get_element(commands, data, var_type)
        if other_indexes is not None:
            for other_index in other_indexes:
                commands.extract_value()
                other_index.compile_vm(commands, data)
                commands.extract_value()
                ArrayCompiler.get_element(commands, data, var_type)
        return Types.DYNAMIC

""" Компиляция built-in функции arrlen для получения длины массива """
def arrlen(commands, data, args):
    array_type = args.elements[0].compile_vm(commands, data)
    commands.extract_value()
    ArrayCompiler.arrlen(commands, data, array_type)

    return commands.set_and_return_type(Types.INT)
