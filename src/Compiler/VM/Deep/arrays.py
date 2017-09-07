# -*- coding: utf-8 -*-

from ..Helpers.base import *
from ..Helpers.loop import Loop

class ArrayCompiler:
    @staticmethod
    def unboxed_arrmake(commands, env, values_type):
        arr_pointer = env.var()
        arr_length = env.var()

        commands.add(Dup)
        # Сохраняем длину массива в переменную
        commands.add(Store, arr_length)

        commands.add(DAllocate, 1)

        if values_type == 'none':
            return

        finish_label = env.label()

        # Сохраняем длину массива в переменную
        commands.add(Store, arr_pointer)

        is_repeated_values = values_type == 'zeros' or values_type == 'repeated'

        if is_repeated_values:
            basis_element = env.var()
            # Сохраняем длину массива в переменную
            commands.add(Store, basis_element)

        def cycle_body(_counter, b, c):
            commands.add(Load, _counter)
            commands.add(Load, arr_length)
            commands.add(Compare, 5)
            commands.add(Jnz, finish_label)
            if is_repeated_values:
                commands.add(Load, basis_element)
            dbstore(arr_pointer, _counter, commands)

        counter = Loop.simple(commands, env, cycle_body, return_counter=True)

        commands.add(Label, finish_label)

        commands.add(Push, 0)
        dbstore(arr_pointer, counter, commands)

        commands.add(Load, arr_pointer)

    @staticmethod
    def element(commands, env):
        # Прибавляем к номеру ячейки с началом строки номер требуемого символа (offset)
        commands.add(Add)
        # Загружаем на стек символ по номеру его ячейки в heap memory
        commands.add(DBLoad, 0)

    @staticmethod
    def arrlen(commands, env):
        arr_start_pointer = env.var()

        # Разыменовываем лежащий на стеке указатель и записываем его в переменную
        commands.add(Store, arr_start_pointer)

        # Считываем строку из памяти до конца (пока не встретим 0), подсчитывая кол-во символов (его кладем на стек)
        Loop.data_heap(commands, env, arr_start_pointer)
