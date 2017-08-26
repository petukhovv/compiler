# -*- coding: utf-8 -*-

from src.VM.Helpers.parser import command_class_relation_map, ARGS_SEPARATOR
from src.VM.commands import *
from environment import Environment

commands_relation_map = dict((command_class_relation_map[k], k) for k in command_class_relation_map)

class Commands(list):
    def add(self, command, argument=None):
        self.append(self.gen(command, argument))
        return self

    @staticmethod
    def gen(command, argument=None):
        argument = '' if argument is None else ARGS_SEPARATOR + str(argument)
        return commands_relation_map[command] + argument

    """
    Генерация команд для организация цикла на стеке.
    Цикл завершается, если на стеке оказалось 0.
    После завершения на стек помещается число совершенных итераций.
    """
    def stack_cycle(self, env, callback, load_counter=True):
        # Создаем метки и переменные, необходимые для прохождения цикла.
        start_while_label = Environment.create_label(env)
        end_while_label = Environment.create_label(env)
        continue_label = Environment.create_label(env)
        counter_var = Environment.create_var(env)

        # Инициализируем счетчик цикла.
        self.add(Push, 0)\
            .add(Store, counter_var)\
            .add(Label, start_while_label)

        # Выполняем тело цикла.
        callback(counter_var, end_while_label, continue_label)

        self.add(Label, continue_label)

        # Инкрементируем счетчик цикла.
        self.add(Load, counter_var)\
            .add(Push, 1)\
            .add(Add)\
            .add(Store, counter_var)

        # Если после выполнения callback на стеке 0 - завершаем цикл.
        self.add(Dup)\
            .add(Jz, end_while_label)\
            .add(Jump, start_while_label)\
            .add(Label, end_while_label)

        # Очищаем оставшийся на стеке 0 (поскольку перед Jz использовали Dup).
        self.add(Pop)

        # Если требуется, загружаем на стек количество совершенных итераций.
        if load_counter:
            self.add(Load, counter_var)

        return self

    """
    Генерация команд для организация цикла в памяти.
    Цикл завершается, если в очередной ячейке памяти оказалось 0.
    После завершения на стек помещается число совершенных итераций.
    """
    def memory_cycle(self, env, var_number, callback=None, load_counter=True):
        # Создаем метки и переменные, необходимые для прохождения цикла.
        start_while_label = Environment.create_label(env)
        end_while_label = Environment.create_label(env)
        continue_label = Environment.create_label(env)
        counter_var = Environment.create_var(env)

        # Инициализируем счетчик цикла.
        self.add(Push, 0)\
            .add(Store, counter_var)\
            .add(Label, start_while_label)

        # Выполняем тело цикла.
        if callback is not None:
            callback(counter_var, end_while_label, continue_label)

        self.add(Label, continue_label)

        # Если после выполнения callback в ячейке памяти 0 - завершаем цикл.
        self.add(Load, var_number)\
            .add(Load, counter_var)\
            .add(Sub) \
            .add(BLoad, 0)\
            .add(Jz, end_while_label)

        # Инкрементируем счетчик цикла.
        self.add(Load, counter_var) \
            .add(Push, 1) \
            .add(Add) \
            .add(Store, counter_var)

        self.add(Jump, start_while_label)\
            .add(Label, end_while_label)

        # Если требуется, загружаем на стек количество совершенных итераций.
        if load_counter:
            self.add(Load, counter_var)

        return self