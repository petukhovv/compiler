# -*- coding: utf-8 -*-

from ..Helpers.base import *
from ..Helpers.loop import Loop
from ..Core.registers import Registers
from ..Utils.malloc import Malloc


class ArrayCompiler:
    ELEMENT_SIZE = 4

    @staticmethod
    def arrmake(compiler, default_values_variant):
        """
        Генерация инструкций для выделения памяти под boxed и unboxed массивы и записи в него значений по умолчанию
        """
        arr_length = compiler.environment.add_local_var(Types.INT)

        compiler.code.add(Commands.POP, arr_length)

        is_repeated_values = default_values_variant == 'zeros' or default_values_variant == 'repeated'
        if is_repeated_values:
            basis_element = compiler.environment.add_local_var(Types.INT)
            compiler.code.add(Commands.POP, basis_element)

        # Сохраняем длину массива в переменную
        compiler.code.add(Commands.MOV, [Registers.EAX, arr_length])\
            .add(Commands.MOV, [Registers.EBX, 2 * ArrayCompiler.ELEMENT_SIZE])\
            .add(Commands.MUL, Registers.EBX)\
            .add(Commands.ADD, [Registers.EAX, ArrayCompiler.ELEMENT_SIZE])
        # Выделяем память = переданной длине массива * 2 * ArrayCompiler.ELEMENT_SIZE + 1 (плюс тип под каждое значение и длина массива)
        Malloc(compiler).call()

        # Если значения по умолчанию не заданы, оставляем элементы массива пустыми и выходим
        if default_values_variant == 'none':
            compiler.code.add(Commands.MOV, [Registers.EBX, arr_length])\
                .add(Commands.MOV, ['dword [%s]' % Registers.EAX, Registers.EBX])\
                .add(Commands.PUSH, Registers.EAX)
            return

        arr_pointer = compiler.environment.add_local_var(Types.INT)
        finish_label = compiler.labels.create()

        # Сохраняем указатель на начало массива
        compiler.code.add(Commands.MOV, [arr_pointer, Registers.EAX])

        def cycle_body(_counter, b, c):
            compiler.code.add(Commands.MOV, [Registers.EAX, _counter])\
                .add(Commands.MOV, [Registers.EBX, arr_length])\
                .add(Commands.CMP, [Registers.EAX, Registers.EBX])\
                .add(Commands.JZ, finish_label)

            # Расчитываем адрес, по которому располагается текущий элемент
            element_address = calc_arr_element_address(compiler, arr_pointer, _counter)

            # В случае если элементы должны быть одинаковыми, загружаем базисное значение,
            # в противном случае (при полном задании default values) значения уже будут находиться на стеке
            if is_repeated_values:
                compiler.code.add(Commands.MOV, [Registers.EAX, element_address])\
                    .add(Commands.ADD, [Registers.EAX, ArrayCompiler.ELEMENT_SIZE])\
                    .add(Commands.MOV, ['dword [%s]' % Registers.EAX, Types.INT])\
                    .add(Commands.ADD, [Registers.EAX, ArrayCompiler.ELEMENT_SIZE])\
                    .add(Commands.MOV, [Registers.EBX, basis_element])\
                    .add(Commands.MOV, ['dword [%s]' % Registers.EAX, Registers.EBX])

        Loop.simple(compiler, cycle_body)

        compiler.code.add_label(finish_label)

        # Сохраняем длину массива в первую ячейку памяти, где располагается массив
        compiler.code.add(Commands.MOV, [Registers.EAX, arr_length])\
            .add(Commands.MOV, [Registers.EBX, arr_pointer])\
            .add(Commands.MOV, ['dword [%s]' % Registers.EBX, Registers.EAX])

        # Загружаем на стек указатель на начало массива
        compiler.code.add(Commands.PUSH, arr_pointer)

    @staticmethod
    def get_element(compiler, type):
        """ Генерация инструкций для оператора получения элемента массива: A[n] """
        # Расчитываем адрес элемента (с учетом хранения типов для каждого элемента - умножаем на 2)
        compiler.code.add(Commands.POP, Registers.EAX)\
            .add(Commands.MOV, [Registers.EBX, 2 * ArrayCompiler.ELEMENT_SIZE])\
            .add(Commands.MUL, Registers.EBX)\
            .add(Commands.ADD, [Registers.EAX, ArrayCompiler.ELEMENT_SIZE])
        # Прибавляем к номеру ячейки с началом массива индекс требуемого значения (offset)
        compiler.code.add(Commands.POP, Registers.EBX)\
            .add(Commands.ADD, [Registers.EBX, Registers.EAX])
        # Загружаем на стек значение элемента по адресу его ячейки в heap memory
        compiler.code.add(Commands.ADD, [Registers.EBX, ArrayCompiler.ELEMENT_SIZE])\
            .add(Commands.MOV, [Registers.EAX, 'dword [%s]' % Registers.EBX])\
            .add(Commands.PUSH, Registers.EAX)
        # Загружаем на стек тип элемента по адресу его ячейки в heap memory
        compiler.code.add(Commands.SUB, [Registers.EBX, ArrayCompiler.ELEMENT_SIZE])\
            .add(Commands.MOV, [Registers.EAX, 'dword [%s]' % Registers.EBX])\
            .add(Commands.PUSH, Registers.EAX)

    @staticmethod
    def set_element(compiler, type):
        """ Генерация инструкций для присвоения значения элементу массива: A[n] := x """
        # Записываем в heap memory тип элемента по адресу его ячейки в heap memory
        compiler.code.add(Commands.ADD, [Registers.EAX, ArrayCompiler.ELEMENT_SIZE])\
            .add(Commands.POP, Registers.EBX)\
            .add(Commands.MOV, ['dword [%s]' % Registers.EAX, Registers.EBX])
        # Записываем в heap memory значение элемента по адресу его ячейки в heap memory
        compiler.code.add(Commands.SUB, [Registers.EAX, ArrayCompiler.ELEMENT_SIZE])\
            .add(Commands.POP, Registers.EBX)\
            .add(Commands.MOV, ['dword [%s]' % Registers.EAX, Registers.EBX])

    @staticmethod
    def arrlen(compiler):
        """ Генерация инструкций для получения длины массива """
        compiler.code.add(Commands.POP, Registers.EAX)\
            .add(Commands.MOV, [Registers.EAX, 'dword [%s]' % Registers.EAX])\
            .add(Commands.PUSH, Registers.EAX)

    @staticmethod
    def calc_element_place(compiler):
        compiler.code.add(Commands.POP, Registers.EAX) \
            .add(Commands.MOV, [Registers.ECX, 2 * ArrayCompiler.ELEMENT_SIZE]) \
            .add(Commands.MUL, Registers.ECX) \
            .add(Commands.ADD, [Registers.EAX, ArrayCompiler.ELEMENT_SIZE]) \
            .add(Commands.POP, Registers.EBX) \
            .add(Commands.ADD, [Registers.EBX, Registers.EAX])
