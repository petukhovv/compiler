# -*- coding: utf-8 -*-

from ..Helpers.base import *
from ..Helpers.loop import Loop
from ..Utils.malloc import Malloc
from ..Helpers.commands import Commands


class ArrayCompiler:
    @staticmethod
    def arrmake(compiler, default_values_variant):
        """
        Генерация инструкций для выделения памяти под boxed и unboxed массивы и записи в него значений по умолчанию
        """
        arr_length = compiler.bss.vars.add(None, 'resb', 4, Types.INT)

        compiler.code.add(Commands.POP, ['dword [%s]' % arr_length])

        is_repeated_values = default_values_variant == 'zeros' or default_values_variant == 'repeated'
        if is_repeated_values:
            basis_element = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
            compiler.code.add(Commands.POP, ['dword [%s]' % basis_element])

        # Сохраняем длину массива в переменную
        compiler.code.add(Commands.MOV, ['eax', 'dword [%s]' % arr_length])
        compiler.code.add(Commands.MOV, ['ebx', 2 * 4])
        compiler.code.add(Commands.MUL, ['ebx'])
        compiler.code.add(Commands.ADD, ['eax', 4])
        # Выделяем память = переданной длине массива * 2 * 4 + 1 (плюс тип под каждое значение и длина массива)
        Malloc(compiler).call()

        # Если значения по умолчанию не заданы, оставляем элементы массива пустыми и выходим
        if default_values_variant == 'none':
            compiler.code.add(Commands.MOV, ['ebx', 'dword [%s]' % arr_length])
            compiler.code.add(Commands.MOV, ['dword [eax]', 'ebx'])
            compiler.code.add(Commands.PUSH, ['eax'])
            return

        arr_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        finish_label = compiler.labels.create()

        # Сохраняем указатель на начало массива
        compiler.code.add(Commands.MOV, ['dword [%s]' % arr_pointer, 'eax'])

        def cycle_body(_counter, b, c):
            compiler.code.add(Commands.MOV, ['eax', 'dword [%s]' % _counter])
            compiler.code.add(Commands.MOV, ['ebx', 'dword [%s]' % arr_length])
            compiler.code.add(Commands.CMP, ['eax', 'ebx'])
            compiler.code.add(Commands.JZ, [finish_label])

            # Расчитываем адрес, по которому располагается текущий элемент
            element_address = calc_arr_element_address(compiler, arr_pointer, _counter)

            # В случае если элементы должны быть одинаковыми, загружаем базисное значение,
            # в противном случае (при полном задании default values) значения уже будут находиться на стеке
            if is_repeated_values:
                compiler.code.add(Commands.MOV, ['eax', 'dword [%s]' % element_address])
                compiler.code.add(Commands.ADD, ['eax', 4])
                compiler.code.add(Commands.MOV, ['dword [eax]', Types.INT])
                compiler.code.add(Commands.ADD, ['eax', 4])
                compiler.code.add(Commands.MOV, ['ebx', 'dword [%s]' % basis_element])
                compiler.code.add(Commands.MOV, ['dword [eax]', 'ebx'])

        Loop.simple(compiler, cycle_body)

        compiler.code.add(str(finish_label) + ':', [])

        # Сохраняем длину массива в первую ячейку памяти, где располагается массив
        compiler.code.add(Commands.MOV, ['eax', 'dword [%s]' % arr_length])
        compiler.code.add(Commands.MOV, ['ebx', 'dword [%s]' % arr_pointer])
        compiler.code.add(Commands.MOV, ['dword [ebx]', 'eax'])

        # Загружаем на стек указатель на начало массива
        compiler.code.add(Commands.PUSH, ['dword [%s]' % arr_pointer])

    @staticmethod
    def get_element(compiler, type):
        """ Генерация инструкций для оператора получения элемента массива: A[n] """
        # Расчитываем адрес элемента (с учетом хранения типов для каждого элемента - умножаем на 2)
        compiler.code.add(Commands.POP, ['eax'])
        compiler.code.add(Commands.MOV, ['ebx', 2 * 4])
        compiler.code.add(Commands.MUL, ['ebx'])
        compiler.code.add(Commands.ADD, ['eax', 4])
        # Прибавляем к номеру ячейки с началом массива индекс требуемого значения (offset)
        compiler.code.add(Commands.POP, ['ebx'])
        compiler.code.add(Commands.ADD, ['ebx', 'eax'])
        # Загружаем на стек значение элемента по адресу его ячейки в heap memory
        compiler.code.add(Commands.ADD, ['ebx', 4])
        compiler.code.add(Commands.MOV, ['eax', 'dword [ebx]'])
        compiler.code.add(Commands.PUSH, ['eax'])
        # Загружаем на стек тип элемента по адресу его ячейки в heap memory
        compiler.code.add(Commands.SUB, ['ebx', 4])
        compiler.code.add(Commands.MOV, ['eax', 'dword [ebx]'])
        compiler.code.add(Commands.PUSH, ['eax'])

    @staticmethod
    def set_element(compiler, type):
        """ Генерация инструкций для присвоения значения элементу массива: A[n] := x """
        # Расчитываем адрес элемента (с учетом хранения типов для каждого элемента - умножаем на 2)
        compiler.code.add(Commands.POP, ['eax'])
        compiler.code.add(Commands.MOV, ['ebx', 2 * 4])
        compiler.code.add(Commands.MUL, ['ebx'])
        compiler.code.add(Commands.ADD, ['eax', 4])
        # Прибавляем к номеру ячейки с началом массива индекс требуемого значения (offset)
        compiler.code.add(Commands.POP, ['ebx'])
        compiler.code.add(Commands.ADD, ['eax', 'ebx'])

        # Записываем в heap memory тип элемента по адресу его ячейки в heap memory
        compiler.code.add(Commands.ADD, ['eax', 4])
        compiler.code.add(Commands.POP, ['ebx'])
        compiler.code.add(Commands.MOV, ['dword [eax]', 'ebx'])
        # Записываем в heap memory значение элемента по адресу его ячейки в heap memory
        compiler.code.add(Commands.SUB, ['eax', 4])
        compiler.code.add(Commands.POP, ['ebx'])
        compiler.code.add(Commands.MOV, ['dword [eax]', 'ebx'])

    @staticmethod
    def arrlen(compiler):
        """ Генерация инструкций для получения длины массива """
        compiler.code.add(Commands.POP, ['eax'])
        compiler.code.add(Commands.MOV, ['eax', 'dword [eax]'])
        compiler.code.add(Commands.PUSH, ['eax'])
