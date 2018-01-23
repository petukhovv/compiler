# -*- coding: utf-8 -*-

from ..Helpers.base import *
from ..Helpers.loop import Loop
from ..Utils.malloc import Malloc


class ArrayCompiler:
    @staticmethod
    def arrmake(compiler, default_values_variant):
        """ Генерация инструкций для выделения памяти под boxed и unboxed массивы и записи в него значений по умолчанию """
        arr_length = compiler.bss.vars.add(None, 'resb', 4, Types.INT)

        compiler.code.add('pop', ['dword [%s]' % arr_length])

        is_repeated_values = default_values_variant == 'zeros' or default_values_variant == 'repeated'
        if is_repeated_values:
            basis_element = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
            compiler.code.add('pop', ['dword [%s]' % basis_element])

        # Сохраняем длину массива в переменную
        compiler.code.add('mov', ['eax', 'dword [%s]' % arr_length])
        compiler.code.add('mov', ['ebx', 2 * 4])
        compiler.code.add('mul', ['ebx'])
        compiler.code.add('add', ['eax', 4])
        # Выделяем память = переданной длине массива * 2 * 4 + 1 (плюс тип под каждое значение и длина массива)
        Malloc(compiler).call()

        # Если значения по умолчанию не заданы, оставляем элементы массива пустыми и выходим
        if default_values_variant == 'none':
            compiler.code.add('mov', ['ebx', 'dword [%s]' % arr_length])
            compiler.code.add('mov', ['dword [eax]', 'ebx'])
            compiler.code.add('push', ['eax'])
            return

        arr_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        finish_label = compiler.labels.create()

        # Сохраняем указатель на начало массива
        compiler.code.add('mov', ['dword [%s]' % arr_pointer, 'eax'])

        def cycle_body(_counter, b, c):
            compiler.code.add('mov', ['eax', 'dword [%s]' % _counter])
            compiler.code.add('mov', ['ebx', 'dword [%s]' % arr_length])
            compiler.code.add('cmp', ['eax', 'ebx'])
            compiler.code.add('jz near', [finish_label])

            # Расчитываем адрес, по которому располагается текущий элемент
            element_address = calc_arr_element_address(compiler, arr_pointer, _counter)

            # В случае если элементы должны быть одинаковыми, загружаем базисное значение,
            # в противном случае (при полном задании default values) значения уже будут находиться на стеке
            if is_repeated_values:
                compiler.code.add('mov', ['eax', 'dword [%s]' % element_address])
                compiler.code.add('add', ['eax', 4])
                compiler.code.add('mov', ['dword [eax]', Types.INT])
                compiler.code.add('add', ['eax', 4])
                compiler.code.add('mov', ['ebx', 'dword [%s]' % basis_element])
                compiler.code.add('mov', ['dword [eax]', 'ebx'])

        Loop.simple(compiler, cycle_body)

        compiler.code.add(str(finish_label) + ':', [])

        # Сохраняем длину массива в первую ячейку памяти, где располагается массив
        compiler.code.add('mov', ['eax', 'dword [%s]' % arr_length])
        compiler.code.add('mov', ['ebx', 'dword [%s]' % arr_pointer])
        compiler.code.add('mov', ['dword [ebx]', 'eax'])

        # Загружаем на стек указатель на начало массива
        compiler.code.add('push', ['dword [%s]' % arr_pointer])

    @staticmethod
    def get_element(compiler, type):
        """ Генерация инструкций для оператора получения элемента массива: A[n] """
        # Расчитываем адрес элемента (с учетом хранения типов для каждого элемента - умножаем на 2)
        compiler.code.add('pop', ['eax'])
        compiler.code.add('mov', ['ebx', 2 * 4])
        compiler.code.add('mul', ['ebx'])
        compiler.code.add('add', ['eax', 4])
        # Прибавляем к номеру ячейки с началом массива индекс требуемого значения (offset)
        compiler.code.add('pop', ['ebx'])
        compiler.code.add('add', ['ebx', 'eax'])
        # Загружаем на стек значение элемента по адресу его ячейки в heap memory
        compiler.code.add('add', ['ebx', 4])
        compiler.code.add('mov', ['eax', 'dword [ebx]'])
        compiler.code.add('push', ['eax'])
        # Загружаем на стек тип элемента по адресу его ячейки в heap memory
        compiler.code.add('sub', ['ebx', 4])
        compiler.code.add('mov', ['eax', 'dword [ebx]'])
        compiler.code.add('push', ['eax'])

    @staticmethod
    def set_element(compiler, type):
        """ Генерация инструкций для присвоения значения элементу массива: A[n] := x """
        # Расчитываем адрес элемента (с учетом хранения типов для каждого элемента - умножаем на 2)
        compiler.code.add('pop', ['eax'])
        compiler.code.add('mov', ['ebx', 2 * 4])
        compiler.code.add('mul', ['ebx'])
        compiler.code.add('add', ['eax', 4])
        # Прибавляем к номеру ячейки с началом массива индекс требуемого значения (offset)
        compiler.code.add('pop', ['ebx'])
        compiler.code.add('add', ['eax', 'ebx'])

        # Записываем в heap memory тип элемента по адресу его ячейки в heap memory
        compiler.code.add('add', ['eax', 4])
        compiler.code.add('pop', ['ebx'])
        compiler.code.add('mov', ['dword [eax]', 'ebx'])
        # Записываем в heap memory значение элемента по адресу его ячейки в heap memory
        compiler.code.add('sub', ['eax', 4])
        compiler.code.add('pop', ['ebx'])
        compiler.code.add('mov', ['dword [eax]', 'ebx'])

    @staticmethod
    def arrlen(compiler):
        """ Генерация инструкций для получения длины массива """
        compiler.code.add('pop', ['eax'])
        compiler.code.add('mov', ['eax', 'dword [eax]'])
        compiler.code.add('push', ['eax'])
