# -*- coding: utf-8 -*-

from src.VM.Helpers.parser import command_class_relation_map, ARGS_SEPARATOR
from src.VM.commands import *
from env import Env

commands_relation_map = dict((command_class_relation_map[k], k) for k in command_class_relation_map)

class Commands(list):
    load_commands = {
        'stack': BLoad,
        'heap': DBLoad
    }

    def add(self, command, argument=None):
        self.append(self.gen(command, argument))
        return self

    @staticmethod
    def gen(command, argument=None):
        argument = '' if argument is None else ARGS_SEPARATOR + str(argument)
        return commands_relation_map[command] + argument

    """
    Генерация команд для организации цикла.
    Условие останова - динамическое, передается извне.
    """
    def loop_base(self, env, check_break_condition, callback, load_counter=True, return_counter=False):
        # Создаем метки и переменные, необходимые для прохождения цикла.
        counter = Env.var(env)

        start_label = Env.label(env)
        finish_label = Env.label(env)
        continue_label = Env.label(env)

        # Инициализируем счетчик цикла
        self.add(Push, 0) \
            .add(Store, counter) \
            .add(Label, start_label)

        # Выполняем тело цикла
        if callback is not None:
            callback(counter, finish_label, continue_label)

        self.add(Label, continue_label)

        # Инкрементируем счетчик цикла
        self.add(Load, counter) \
            .add(Push, 1) \
            .add(Add) \
            .add(Store, counter)

        # Выполняем переданное условие останова
        if check_break_condition is not None:
            check_break_condition(start_label, finish_label, counter)

        self.add(Jump, start_label) \
            .add(Label, finish_label)

        # Если требуется, загружаем на стек количество совершенных итераций
        if load_counter:
            self.add(Load, counter)

        # Если требуется, возвращаем переменную, в которой содержится кол-во совершенных итераций
        if return_counter:
            return counter

        return self

    """
    Генерация команд для организация произвольного цикла.
    Критерий отстанова и сам останов должен реализовываться внутри callback.
    """
    def loop(self, env, callback, return_counter=False):
        return self.loop_base(env, None, callback, False, return_counter)

    """
    Генерация команд для организация цикла на стеке.
    Цикл завершается, если на стеке оказалось 0.
    """
    def loop_stack(self, env, callback, load_counter=True, return_counter=False):
        def check_break_condition(a, finish_label, b):
            # Если после выполнения callback на стеке 0 - завершаем цикл.
            self.add(Dup).add(Jz, finish_label)

        result = self.loop_base(env, check_break_condition, callback, load_counter, return_counter)

        # Очищаем оставшийся на стеке 0 (поскольку перед Jz использовали Dup).
        self.add(Pop)

        return result

    """
    Генерация команд для организация цикла в памяти.
    Цикл завершается, если в очередной ячейке стековой памяти оказалось 0.
    """
    def loop_data(self, env, start_pointer, callback=None, load_counter=True, return_counter=False, memory_type='heap'):
        def check_break_condition(a, finish_label, _counter):
            # Если после выполнения callback в ячейке памяти 0 - завершаем цикл.
            self.add(Load, start_pointer) \
                .add(Load, _counter) \
                .add(Add) \
                .add(self.load_commands[memory_type], 0) \
                .add(Jz, finish_label)

        return self.loop_base(env, check_break_condition, callback, load_counter, return_counter)

    """
    Генерация команд для организация цикла в памяти.
    Цикл завершается, если в очередной ячейке стековой памяти оказалось 0.
    """
    def loop_data_stack(self, env, start_pointer, callback=None, load_counter=True, return_counter=False):
        return self.loop_data(env, start_pointer, callback, load_counter, return_counter, memory_type='stack')

    """
    Генерация команд для организация цикла в памяти.
    Цикл завершается, если в очередной ячейке heap-памяти оказалось 0.
    """
    def loop_data_heap(self, env, start_pointer, callback=None, load_counter=True, return_counter=False):
        return self.loop_data(env, start_pointer, callback, load_counter, return_counter)
