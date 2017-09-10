# -*- coding: utf-8 -*-

from ..Helpers.base import *
from ..Helpers.loop import Loop

class ArrayCompiler:
    """
    Генерация инструкций для выделения памяти под unboxed-массив и записи в него значений по умолчанию
    """
    @staticmethod
    def unboxed_arrmake(commands, env, values_type):
        arr_length = env.var(types.INT)

        commands.add(Dup)
        # Сохраняем длину массива в переменную
        commands.add(Store, arr_length)
        # Выделяем память = переданной длине массива +1 (плюс маркер конца массива - 0)
        commands.add(DAllocate, 1)

        # Если значения по умолчанию не заданы, оставляем элементы массива пустыми и выходим
        if values_type == 'none':
            return

        arr_pointer = env.var(types.INT)

        finish_label = env.label()

        # Сохраняем указатель на начало массива
        commands.add(Store, arr_pointer)

        is_repeated_values = values_type == 'zeros' or values_type == 'repeated'

        # Если все элементы должны быть одинаковыми, равными одному значению (basis_element), загружаем его
        if is_repeated_values:
            basis_element = env.var(types.CHAR)
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
            dbstore(arr_pointer, _counter, commands)

        counter = Loop.simple(commands, env, cycle_body, return_counter=True)

        commands.add(Label, finish_label)

        # Записываем маркер конца массива - 0
        commands.add(Push, 0)
        dbstore(arr_pointer, counter, commands)

        commands.add(Load, arr_pointer)

    """
    Генерация инструкций для оператора получения элемента массива: A[n]
    """
    @staticmethod
    def get_element(commands, env):
        # Прибавляем к номеру ячейки с началом массива индекс требуемого значения (offset)
        commands.add(Add)
        # Загружаем на стек значение по номеру его ячейки в heap memory
        commands.add(DBLoad, 0)

    """
    Генерация инструкций для присвоения значения элементу массива: A[n] := t
    """
    @staticmethod
    def set_element(commands, env):
        # Прибавляем к номеру ячейки с началом массива индекс требуемого значения (offset)
        commands.add(Add)
        # Записываем в heap memory значение по номеру его ячейки
        commands.add(DBStore, 0)

    """
    Генерация инструкций для получения длина массива
    """
    @staticmethod
    def arrlen(commands, env):
        arr_start_pointer = env.var(types.INT)

        # Записываем указатель на начало массива в переменную
        commands.add(Store, arr_start_pointer)

        # Считываем массив из памяти до конца (пока не встретим 0), подсчитывая кол-во элементов (его кладем на стек)
        Loop.data_heap(commands, env, arr_start_pointer)
