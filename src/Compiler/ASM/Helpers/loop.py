# -*- coding: utf-8 -*-

from ..Core.registers import Registers
from ..Core.types import *


class Loop:
    @staticmethod
    def base(compiler, check_break_condition, callback, load_counter=True, return_counter=False):
        """
        Генерация команд для организации цикла.
        Условие останова - динамическое, передается извне.
        """
        # Создаем метки и переменные, необходимые для прохождения цикла.
        counter = compiler.vars.add(None, 'resb', 4, Types.INT)

        start_label = compiler.labels.create()
        finish_label = compiler.labels.create()
        continue_label = compiler.labels.create()

        # Инициализируем счетчик цикла
        compiler.code.add(Commands.MOV, ['dword [%s]' % counter, 0])\
            .add_label(start_label)

        # Выполняем тело цикла
        if callback is not None:
            callback(counter, finish_label, continue_label)

        compiler.code.add_label(continue_label)

        # Инкрементируем счетчик цикла
        compiler.code.add(Commands.MOV, [Registers.EAX, 'dword [%s]' % counter])\
            .add(Commands.ADD, [Registers.EAX, 1])\
            .add(Commands.MOV, ['dword [%s]' % counter, Registers.EAX])

        # Выполняем переданное условие останова
        if check_break_condition is not None:
            check_break_condition(start_label, finish_label, counter)

        compiler.code.add(Commands.JMP, start_label)\
            .add_label(finish_label)

        # Если требуется, загружаем на стек количество совершенных итераций
        if load_counter:
            compiler.code.add(Commands.PUSH, ['dword [%s]' % counter])

        # Если требуется, возвращаем переменную, в которой содержится кол-во совершенных итераций
        if return_counter:
            return counter

    @staticmethod
    def simple(compiler, callback, return_counter=False):
        """
        Генерация команд для организация произвольного цикла.
        Критерий отстанова и сам останов должен реализовываться внутри callback.
        """
        return Loop.base(compiler, None, callback, False, return_counter)

    @staticmethod
    def stack(compiler, callback, load_counter=True, return_counter=False):
        """
        Генерация команд для организация цикла на стеке.
        Цикл завершается, если на стеке оказалось 0.
        """
        def check_break_condition(a, finish_label, b):
            # Если после выполнения callback на стеке 0 - завершаем цикл.
            compiler.code.add(Commands.POP, Registers.EAX)\
                .add(Commands.PUSH, Registers.EAX)\
                .add(Commands.CMP, [Registers.EAX, 0])\
                .add(Commands.JZ, finish_label)

        result = Loop.base(compiler, check_break_condition, callback, load_counter, return_counter)

        # Очищаем оставшийся на стеке 0 (поскольку перед Jz использовали Dup).
        compiler.code.add(Commands.POP, Registers.EAX)

        return result

    @staticmethod
    def data(compiler, start_pointer, callback=None, load_counter=True, return_counter=False):
        """
        Генерация команд для организация цикла в памяти.
        Цикл завершается, если в очередной ячейке стековой памяти оказалось 0.
        """
        def check_break_condition(a, finish_label, _counter):
            # Если после выполнения callback в ячейке памяти 0 - завершаем цикл.
            compiler.code.add(Commands.MOV, [Registers.EAX, 'dword [%s]' % start_pointer])\
                .add(Commands.MOV, [Registers.EBX, 'dword [%s]' % _counter])\
                .add(Commands.ADD, [Registers.EAX, Registers.EBX])\
                .add(Commands.MOVZX, [Registers.EAX, 'byte [%s]' % Registers.EAX])\
                .add(Commands.CMP, [Registers.EAX, 0])\
                .add(Commands.JZ, finish_label)

        return Loop.base(compiler, check_break_condition, callback, load_counter, return_counter)
