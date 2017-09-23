# -*- coding: utf-8 -*-

from Deep.arrays import *

""" Компиляция built-in функции arrmake / Arrmake для создания boxed и unboxed массивов """
def arrmake(commands, data, args, type):
    type = Types.BOXED_ARR if type == 'boxed' else Types.UNBOXED_ARR

    # Если были переданы default values (2-м аргументом), смотрим, в каком именно формате
    if len(args.elements) == 2:
        default_value_type = args.elements[1].compile_vm(commands, data)
        commands.extract_value()
        # Если вторым аргументом был передан [] или {}, то дублируемым элементом будет 0
        # ( сигнатура: arrmake(n, []), Arrmake(n, {}) )
        if default_value_type == type and len(args.elements[1].elements.elements) == 0:
            # Очищаем указатель на пустой массив
            # TODO: после реализации GC сделать здесь delete массива
            commands.add(Pop)
            commands.add(Push, 0)
            default_values_variant = 'zeros'
        # Если передано [n1, n2, ...] или {a1, a2, ...}, то массив уже создан, возвращаем тип и выходим
        elif default_value_type == type:
            return type
        # Если был передан не массив, а число (или указатель), то оно и будет дублируемым элементом
        else:
            default_values_variant = 'repeated'
    # Если ничего не было передано, то элементы массива будет пустыми (None)
    else:
        default_values_variant = 'none'

    args.elements[0].compile_vm(commands, data)
    commands.extract_value()

    ArrayCompiler.arrmake(commands, data, default_values_variant)

    return commands.set_and_return_type(type)

""" Компиляция конструкции inline задания boxed и unboxed массивов: [n1, n2, ...] / {a1, a2, ...}  """
def arrmake_inline(commands, data, elements, type):
    type = Types.BOXED_ARR if type == 'boxed' else Types.UNBOXED_ARR

    arr_elements = elements.compile_vm(commands, data)

    for element in reversed(arr_elements):
        if type == Types.BOXED_ARR:
            element = data.get_var(element)
            element_type = data.get_type(element)
            commands.add(Load, element)
        else:
            element_type = Types.DYNAMIC
            commands.add(Push, element)
        commands.add(Push, element_type)

    commands.add(Push, len(arr_elements))

    # Сохраняем записанные на стек элементы в память
    ArrayCompiler.arrmake(commands, data, 'preset')

    return commands.set_and_return_type(type)

""" Компиляция оператора получения элемента массива: A[n] """
def array_element(commands, data, array, index, other_indexes, context):
    var_number = data.get_var(array)
    var_type = data.get_type(var_number)

    # Компилируем получение указателя на начало массива
    commands.load_value(var_number)
    commands.extract_value()

    # Компилируем получение индекса
    index.compile_vm(commands, data)
    commands.extract_value()

    def other_index_compile(other_index):
        commands.extract_value()
        other_index.compile_vm(commands, data)
        commands.extract_value()

    if context == 'assign':
        # Если несколько последовательных индексов, разыменовываем каждый
        if other_indexes is not None:
            for other_index in other_indexes:
                ArrayCompiler.get_element(commands, data, var_type)
                other_index_compile(other_index)
        ArrayCompiler.set_element(commands, data, var_type)
    else:
        ArrayCompiler.get_element(commands, data, var_type)
        # Если несколько последовательных индексов, разыменовываем каждый
        if other_indexes is not None:
            for other_index in other_indexes:
                other_index_compile(other_index)
                ArrayCompiler.get_element(commands, data, var_type)

    return Types.DYNAMIC

""" Компиляция built-in функции arrlen для получения длины массива """
def arrlen(commands, data, args):
    args.elements[0].compile_vm(commands, data)
    commands.extract_value()

    ArrayCompiler.arrlen(commands, data)

    return commands.set_and_return_type(Types.INT)
