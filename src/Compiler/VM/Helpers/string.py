# -*- coding: utf-8 -*-

from src.VM.Helpers.assembler import *
from environment import *

class String:
    @staticmethod
    def compile_strlen(commands, env):
        start_while_label = Environment.create_label(env)
        end_while_label = Environment.create_label(env)
        counter_var = Environment.create_var(env)

        commands.append(assemble(Push, 0))
        commands.append(assemble(Store, counter_var))
        commands.append(assemble(Label, start_while_label))
        commands.append(assemble(Dup))
        commands.append(assemble(Jz, end_while_label))
        commands.append(assemble(Pop))
        commands.append(assemble(Load, counter_var))
        commands.append(assemble(Push, 1))
        commands.append(assemble(Add))
        commands.append(assemble(Store, counter_var))
        commands.append(assemble(Jump, start_while_label))
        commands.append(assemble(Label, end_while_label))
        commands.append(assemble(Pop))
        commands.append(assemble(Load, counter_var))

    @staticmethod
    def compile_strget(commands, env):
        start_while_label = Environment.create_label(env)
        end_while_label = Environment.create_label(env)
        continue_search_symbol_label = Environment.create_label(env)

        counter_var = Environment.create_var(env)
        pos_var = Environment.create_var(env)
        target_symbol_var = Environment.create_var(env)

        # Записываем значение из стека в переменную (это номер позиции нужного символа)
        commands.append(assemble(Store, pos_var))

        # Инициализиуем счетчик цикла
        commands.append(assemble(Push, 0))
        commands.append(assemble(Store, counter_var))

        # Запускаем цикл (перебор символов строки)
        commands.append(assemble(Label, start_while_label))
        commands.append(assemble(Dup))
        commands.append(assemble(Jz, end_while_label))
        # Сверяем значение счетчика с нужным номером символа
        commands.append(assemble(Load, counter_var))
        commands.append(assemble(Load, pos_var))
        commands.append(assemble(Compare, 0))
        # Если не совпадают, то пропускаем секцию записи результата в переменную
        commands.append(assemble(Jz, continue_search_symbol_label))
        commands.append(assemble(Store, target_symbol_var))
        commands.append(assemble(Load, target_symbol_var))
        commands.append(assemble(Label, continue_search_symbol_label))

        # Продолжаем перебирать символы строки
        commands.append(assemble(Pop))
        commands.append(assemble(Load, counter_var))
        commands.append(assemble(Push, 1))
        commands.append(assemble(Add))
        commands.append(assemble(Store, counter_var))
        commands.append(assemble(Jump, start_while_label))

        # Завершаем выполнение цикла, изымаем последнее значение со стека - 0 - маркер начала строки,
        # и помещаем найденный символ на стек (помещается 0, если символа не найдено).
        commands.append(assemble(Label, end_while_label))
        commands.append(assemble(Pop))
        commands.append(assemble(Load, target_symbol_var))

    @staticmethod
    def compile_get(commands, env, var_number):
        start_while_label = Environment.create_label(env)
        end_while_label = Environment.create_label(env)
        counter_var = Environment.create_var(env)
        commands.append(assemble(Push, 0))
        commands.append(assemble(Load, var_number))
        commands.append(assemble(BLoad, 0))
        commands.append(assemble(Push, 0))
        commands.append(assemble(Store, counter_var))
        commands.append(assemble(Label, start_while_label))
        commands.append(assemble(Dup))
        commands.append(assemble(Jz, end_while_label))
        commands.append(assemble(Load, var_number))
        commands.append(assemble(Load, counter_var))
        commands.append(assemble(Push, 1))
        commands.append(assemble(Add))
        commands.append(assemble(Store, counter_var))
        commands.append(assemble(Load, counter_var))
        commands.append(assemble(Add))
        commands.append(assemble(BLoad, 0))
        commands.append(assemble(Jump, start_while_label))
        commands.append(assemble(Label, end_while_label))
        commands.append(assemble(Pop))

    @staticmethod
    def compile_set(commands, env, characters):
        pointer_start_string = 0
        for char in characters:
            var_number = Environment.create_var(env)
            if pointer_start_string == 0:
                pointer_start_string = var_number
            commands.append(assemble(Store, var_number))
        commands.append(assemble(Store, Environment.create_var(env)))
        commands.append(assemble(Push, pointer_start_string))
