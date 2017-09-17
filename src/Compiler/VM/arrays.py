# -*- coding: utf-8 -*-

from Deep.arrays import *

""" Компиляция built-in функции arrmake для создания unboxed-массивов """
def unboxed_arrmake(commands, data, args):
    # Если были переданы default values (2-м аргументом), смотрим, в каком именно формате
    if len(args.elements) == 2:
        default_value_type = args.elements[1].compile_vm(commands, data)
        commands.extract_value()
        # Если вторым аргументом был передан [], то дублируемым элементом будет 0 ( сигнатура: arrmake(n, []) )
        if default_value_type == Types.UNBOXED_ARR_INLINE and len(args.elements[1].elements.elements) == 0:
            commands.add(Push, 0)
            values_type = 'zeros'
        # Если [n1, n2, ...], то будем записывать в элементы заданные значения
        elif default_value_type == Types.UNBOXED_ARR_INLINE and len(args.elements[1].elements.elements) != 0:
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

    return commands.set_and_return_type(Types.UNBOXED_ARR)

""" Компиляция конструкции константного задания unboxed-массива: [n1, n2, ...]  """
def array_inline(commands, data, elements, type):
    arr_elements = elements.compile_vm(commands, data)

    arrlen_var = data.var()
    commands.add(Push, len(arr_elements))
    commands.add(Store, arrlen_var)

    for element in arr_elements:
        commands.add(Push, element)
        commands.add(Store, data.var())

    commands.add(Push, arrlen_var)

    return_type = Types.BOXED_ARR_INLINE if type == 'boxed' else Types.UNBOXED_ARR_INLINE
    return commands.set_and_return_type(return_type)

""" Компиляция оператора получения элемента массива: A[n] """
def array_element(commands, data, array, index, other_indexes, context):
    index.compile_vm(commands, data)
    commands.extract_value()
    var_number = data.get_var(array)
    var_type = data.get_type(var_number)
    commands.load_value(var_number)
    commands.extract_value()
    if context == 'assign':
        ArrayCompiler.set_element(commands, data, var_type)
    else:
        ArrayCompiler.get_element(commands, data, var_type)
        return commands.set_and_return_type(Types.DYNAMIC)

""" Компиляция built-in функции arrlen для получения длины массива """
def arrlen(commands, data, args):
    array_type = args.elements[0].compile_vm(commands, data)
    commands.extract_value()
    ArrayCompiler.arrlen(commands, data, array_type)

    return commands.set_and_return_type(Types.INT)

""" Компиляция built-in функции arrmake для создания unboxed-массивов """
def boxed_arrmake(commands, data, args):
    # Если были переданы default values (2-м аргументом), смотрим, в каком именно формате
    if len(args.elements) == 2:
        default_value_type = args.elements[1].compile_vm(commands, data)
        commands.extract_value()
        # Если вторым аргументом был передан [], то дублируемым элементом будет 0 ( сигнатура: arrmake(n, []) )
        if default_value_type == Types.UNBOXED_ARR_INLINE and len(args.elements[1].elements.elements) == 0:
            commands.add(Push, 0)
            values_type = 'zeros'
        # Если [n1, n2, ...], то будем записывать в элементы заданные значения
        elif default_value_type == Types.UNBOXED_ARR_INLINE and len(args.elements[1].elements.elements) != 0:
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

    return commands.set_and_return_type(Types.UNBOXED_ARR)
