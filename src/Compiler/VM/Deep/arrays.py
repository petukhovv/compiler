# -*- coding: utf-8 -*-

from ..Helpers.types import Types
from ..Helpers.base import calc_arr_element_address
from ..Helpers.loop import Loop
from ..Helpers.commands import Dup, Store, Push, Mul, DMalloc, Load, Compare, DBStore, Add, DBLoad, Jnz, Label


class ArrayCompiler:
    @staticmethod
    def arrmake(commands, data, default_values_variant):
        """ Генерация инструкций для выделения памяти под boxed и unboxed массивы и записи в него значений по умолчанию """
        arr_length = data.var()

        commands.add(Dup)
        # Сохраняем длину массива в переменную
        commands.add(Store, arr_length)
        commands.add(Push, 2)
        commands.add(Mul)
        # Выделяем память = переданной длине массива * 2 + 1 (плюс тип под каждое значение и длина массива)
        commands.add(DMalloc, 1)

        # Если значения по умолчанию не заданы, оставляем элементы массива пустыми и выходим
        if default_values_variant == 'none':
            return

        arr_pointer = data.var(Types.INT)
        finish_label = data.label()

        # Сохраняем указатель на начало массива
        commands.add(Store, arr_pointer)

        is_repeated_values = default_values_variant == 'zeros' or default_values_variant == 'repeated'

        # Если все элементы должны быть одинаковыми, равными одному значению (basis_element), сохраняем его в перменную
        if is_repeated_values:
            basis_element = data.var(Types.CHAR)
            commands.add(Store, basis_element)

        def cycle_body(_counter, b, c):
            commands.add(Load, _counter)
            commands.add(Load, arr_length)
            commands.add(Compare, 5)
            commands.add(Jnz, finish_label)
            # В случае если элементы должны быть одинаковыми, загружаем базисное значение,
            # в противном случае (при полном задании default values) значения уже будут находиться на стеке
            if is_repeated_values:
                commands.add(Load, basis_element)
                commands.add(Push, Types.INT)

            # Расчитываем адрес, по которому располагается текущий элемент
            element_address = calc_arr_element_address(commands, data, arr_pointer, _counter)

            # Сохраняем по вычисленному адресу тип элемента
            commands.add(DBStore, 1)
            commands.add(Load, element_address)
            # Сохраняем по вычисленному адресу значение элемента
            commands.add(DBStore, 2)

        Loop.simple(commands, data, cycle_body)

        commands.add(Label, finish_label)

        # Сохраняем длину массива в первую ячейку памяти, где располагается массив
        commands.add(Load, arr_length)
        commands.add(Load, arr_pointer)
        commands.add(DBStore, 0)

        # Загружаем на стек указатель на начало массива
        commands.add(Load, arr_pointer)

    @staticmethod
    def get_element(commands, data, type):
        """ Генерация инструкций для оператора получения элемента массива: A[n] """
        arr_address = data.var()

        # Расчитываем адрес элемента (с учетом хранения типов для каждого элемента - умножаем на 2)
        commands.add(Push, 2)
        commands.add(Mul)
        # Прибавляем к номеру ячейки с началом массива индекс требуемого значения (offset)
        commands.add(Add)
        commands.add(Dup)
        commands.add(Store, arr_address)
        # Загружаем на стек тип элемента по адресу его ячейки в heap memory
        commands.add(DBLoad, 2)
        commands.add(Load, arr_address)
        # Загружаем на стек значение элемента по адресу его ячейки в heap memory
        commands.add(DBLoad, 1)

    @staticmethod
    def set_element(commands, data, type):
        """ Генерация инструкций для присвоения значения элементу массива: A[n] := x """
        arr_address = data.var()

        # Расчитываем адрес элемента (с учетом хранения типов для каждого элемента - умножаем на 2)
        commands.add(Push, 2)
        commands.add(Mul)
        # Прибавляем к номеру ячейки с началом массива индекс требуемого значения (offset)
        commands.add(Add)
        commands.add(Store, arr_address)
        commands.add(Dup)
        commands.add(Load, arr_address)
        # Записываем в heap memory тип элемента по адресу его ячейки в heap memory
        commands.add(DBStore, 2)
        commands.add(Load, arr_address)
        # Записываем в heap memory значение элемента по адресу его ячейки в heap memory
        commands.add(DBStore, 1)

    @staticmethod
    def arrlen(commands, data):
        """ Генерация инструкций для получения длины массива """
        commands.add(DBLoad, 0)
