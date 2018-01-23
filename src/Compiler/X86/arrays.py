# -*- coding: utf-8 -*-

from .Deep.arrays import *


def arrmake(compiler, args, type):
    """ Компиляция built-in функции arrmake / Arrmake для создания boxed и unboxed массивов """
    type = Types.BOXED_ARR if type == 'boxed' else Types.UNBOXED_ARR

    # Если были переданы default values (2-м аргументом), смотрим, в каком именно формате
    if len(args.elements) == 2:
        default_value_type = args.elements[1].compile_x86(compiler)
        compiler.commands.clean_type()
        # Если вторым аргументом был передан [] или {}, то дублируемым элементом будет 0
        # ( сигнатура: arrmake(n, []), Arrmake(n, {}) )
        if default_value_type == type and len(args.elements[1].elements.elements) == 0:
            # Очищаем указатель на пустой массив
            # TODO: после реализации GC сделать здесь delete массива
            compiler.code.stack_pop()
            compiler.code.add('push', [0])
            default_values_variant = 'zeros'
        # Если передано [n1, n2, ...] или {a1, a2, ...}, то массив уже создан, возвращаем тип и выходим
        elif default_value_type == type:
            return compiler.commands.set_and_return_type(type)
        # Если был передан не массив, а число (или указатель), то оно и будет дублируемым элементом
        else:
            default_values_variant = 'repeated'
    # Если ничего не было передано, то элементы массива будет пустыми (None)
    else:
        default_values_variant = 'none'

    args.elements[0].compile_x86(compiler)
    compiler.commands.clean_type()

    ArrayCompiler.arrmake(compiler, default_values_variant)

    return compiler.commands.set_and_return_type(type)


def arrmake_inline(compiler, elements, type):
    """ Компиляция конструкции inline задания boxed и unboxed массивов: [n1, n2, ...] / {a1, a2, ...}  """
    type = Types.BOXED_ARR if type == 'boxed' else Types.UNBOXED_ARR

    arr_elements = elements.compile_x86(compiler)
    arr_length = len(arr_elements)
    arr_pointer = compiler.bss.vars.add(None, 'resb',
                                        arr_length * 2 * 4 + 4, Types.INT if type == Types.BOXED_ARR else Types.DYNAMIC)

    compiler.code.add('mov', ['dword [%s]' % arr_pointer, arr_length])
    for i, element in enumerate(arr_elements):
        element_place = i * 2 * 4 + 4

        if type == Types.BOXED_ARR:
            element_type = compiler.bss.vars.get_type(element)
            element = compiler.bss.vars.get(element)
            compiler.code.add('mov', ['eax', element_type])
            compiler.code.add('mov', ['ebx', element])
            element_type = 'eax'
            element = 'ebx'
        else:
            element_type = Types.DYNAMIC

        compiler.code.add('mov', ['dword [%s+%d]' % (arr_pointer, element_place), element_type])
        compiler.code.add('mov', ['dword [%s+%d]' % (arr_pointer, element_place + 4), element])

    compiler.code.add('push', [arr_pointer])

    return compiler.commands.set_and_return_type(type)


def array_element(compiler, array, index, other_indexes, context):
    """ Компиляция оператора получения элемента массива: A[n] """
    var_name = compiler.bss.vars.get(array)
    var_type = compiler.bss.vars.get_type(array)

    # Компилируем получение указателя на начало массива
    compiler.code.add('push', [var_name])

    # Компилируем получение индекса
    index.compile_x86(compiler)
    compiler.commands.clean_type()

    def other_index_compile(other_index):
        compiler.commands.clean_type()
        other_index.compile_x86(compiler)
        compiler.commands.clean_type()

    if context == 'assign':
        # Если несколько последовательных индексов, разыменовываем каждый
        if other_indexes is not None:
            for other_index in other_indexes:
                ArrayCompiler.get_element(compiler, var_type)
                other_index_compile(other_index)
        ArrayCompiler.set_element(compiler, var_type)
    else:
        ArrayCompiler.get_element(compiler, var_type)
        # Если несколько последовательных индексов, разыменовываем каждый
        if other_indexes is not None:
            for other_index in other_indexes:
                other_index_compile(other_index)
                ArrayCompiler.get_element(compiler, var_type)

    return Types.DYNAMIC


def arrlen(compiler, args):
    """ Компиляция built-in функции arrlen для получения длины массива """
    args.elements[0].compile_x86(compiler)
    compiler.commands.clean_type()

    ArrayCompiler.arrlen(compiler)

    return compiler.commands.set_and_return_type(Types.INT)
