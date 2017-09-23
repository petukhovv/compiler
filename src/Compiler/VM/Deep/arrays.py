# -*- coding: utf-8 -*-

from ..Helpers.types import *

from ..Helpers.base import *
from ..Helpers.loop import Loop

class ArrayCompiler:
    """
    Генерация инструкций для выделения памяти под unboxed-массив и записи в него значений по умолчанию
    """
    @staticmethod
    def arrmake(commands, data, values_type):
        arr_length = data.var(Types.INT)
        element_place = data.var()

        commands.add(Dup)
        # Сохраняем длину массива в переменную
        commands.add(Store, arr_length)
        commands.add(Push, 2)
        commands.add(Mul)
        # Выделяем память = переданной длине массива +1 (плюс маркер конца массива - 0)
        commands.add(DAllocate, 1)

        # Если значения по умолчанию не заданы, оставляем элементы массива пустыми и выходим
        if values_type == 'none':
            return

        arr_pointer = data.var(Types.INT)

        finish_label = data.label()

        # Сохраняем указатель на начало массива
        commands.add(Store, arr_pointer)

        is_repeated_values = values_type == 'zeros' or values_type == 'repeated'

        # Если все элементы должны быть одинаковыми, равными одному значению (basis_element), загружаем его
        if is_repeated_values:
            basis_element = data.var(Types.CHAR)
            # Сохраняем повторяемое значение в переменную
            commands.add(Store, basis_element)

        def cycle_body(_counter, b, c):
            commands.add(Load, _counter)
            commands.add(Load, arr_length)
            commands.add(Compare, 5)
            commands.add(Jnz, finish_label)
            # В случае если элементы должны быть одинаковыми, загружаем базисное значение,
            # в противном случае, при полном задании default values, они уже будут находиться на стеке
            if is_repeated_values:
                commands.add(Load, basis_element)
                commands.add(Push, Types.INT)

            commands.add(Load, arr_pointer)
            commands.add(Load, _counter)
            commands.add(Push, 2)
            commands.add(Mul)
            commands.add(Add)
            commands.add(Dup)
            commands.add(Store, element_place)

            commands.add(DBStore, 1)
            commands.add(Load, element_place)
            commands.add(DBStore, 2)

        Loop.simple(commands, data, cycle_body)

        commands.add(Label, finish_label)

        commands.add(Load, arr_length)
        dbstore(arr_pointer, None, commands)

        commands.add(Load, arr_pointer)

    """
    Генерация инструкций для оператора получения элемента массива: A[n]
    """
    @staticmethod
    def get_element(commands, data, type):
        arr_address = data.var()

        commands.add(Push, 2)
        commands.add(Mul)
        # Прибавляем к номеру ячейки с началом массива индекс требуемого значения (offset)
        commands.add(Add)
        commands.add(Dup)
        commands.add(Store, arr_address)
        # Загружаем на стек значение по номеру его ячейки в heap memory
        commands.add(DBLoad, 2)
        commands.add(Load, arr_address)
        commands.add(DBLoad, 1)

    """
    Генерация инструкций для присвоения значения элементу массива: A[n] := t
    """
    @staticmethod
    def set_element(commands, data, type):
        arr_address = data.var()

        commands.add(Push, 2)
        commands.add(Mul)
        # Прибавляем к номеру ячейки с началом массива индекс требуемого значения (offset)
        commands.add(Add)
        commands.add(Store, arr_address)
        commands.add(Dup)
        commands.add(Load, arr_address)
        # Записываем в heap memory значение по номеру его ячейки
        commands.add(DBStore, 2)
        commands.add(Load, arr_address)
        commands.add(DBStore, 1)

    """
    Генерация инструкций для получения длина массива
    """
    @staticmethod
    def arrlen(commands, data, type):
        commands.add(DBLoad, 0)
