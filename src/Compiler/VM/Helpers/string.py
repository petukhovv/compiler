# -*- coding: utf-8 -*-

from src.VM.commands import *
from environment import Environment

class String:
    """
    Генерация инструкций для загрузки строки из переменной в стек
    """
    @staticmethod
    def compile_get(commands, env, var_number):
        start_while_label = Environment.create_label(env)
        end_while_label = Environment.create_label(env)
        counter_var = Environment.create_var(env)
        commands.add(Push, 0)
        commands.add(Load, var_number)
        commands.add(BLoad, 0)
        commands.add(Push, 0)
        commands.add(Store, counter_var)
        commands.add(Label, start_while_label)
        commands.add(Dup)
        commands.add(Jz, end_while_label)
        commands.add(Load, var_number)
        commands.add(Load, counter_var)
        commands.add(Push, 1)
        commands.add(Add)
        commands.add(Store, counter_var)
        commands.add(Load, counter_var)
        commands.add(Add)
        commands.add(BLoad, 0)
        commands.add(Jump, start_while_label)
        commands.add(Label, end_while_label)
        commands.add(Pop)

    """
    Генерация инструкций для загрузки строки из стека в перменную
    """
    @staticmethod
    def compile_set(commands, env, characters):
        pointer_start_string = 0
        for char in characters:
            var_number = Environment.create_var(env)
            if pointer_start_string == 0:
                pointer_start_string = var_number
            commands.add(Store, var_number)
        commands.add(Store, Environment.create_var(env))
        commands.add(Push, pointer_start_string)

    """
    Генерация инструкций для получения длины строки, находящейся на стеке
    """
    @staticmethod
    def compile_strlen(commands, env):
        start_while_label = Environment.create_label(env)
        end_while_label = Environment.create_label(env)
        counter_var = Environment.create_var(env)

        commands.add(Push, 0)
        commands.add(Store, counter_var)
        commands.add(Label, start_while_label)
        commands.add(Dup)
        commands.add(Jz, end_while_label)
        commands.add(Pop)
        commands.add(Load, counter_var)
        commands.add(Push, 1)
        commands.add(Add)
        commands.add(Store, counter_var)
        commands.add(Jump, start_while_label)
        commands.add(Label, end_while_label)
        commands.add(Pop)
        commands.add(Load, counter_var)

    """
    Генерация инструкций для получения определенного символа строки, находящейся на стеке
    """
    @staticmethod
    def compile_strget(commands, env):
        start_while_label = Environment.create_label(env)
        end_while_label = Environment.create_label(env)
        continue_search_symbol_label = Environment.create_label(env)

        counter_var = Environment.create_var(env)
        pos_symbol_var = Environment.create_var(env)
        target_symbol_var = Environment.create_var(env)

        # Записываем значение из стека в переменную (это номер позиции нужного символа)
        commands.add(Store, pos_symbol_var)

        # Инициализиуем счетчик цикла
        commands.add(Push, 0)
        commands.add(Store, counter_var)

        # Запускаем цикл (перебор символов строки)
        commands.add(Label, start_while_label)
        commands.add(Dup)
        commands.add(Jz, end_while_label)
        # Сверяем значение счетчика с нужным номером символа
        commands.add(Load, counter_var)
        commands.add(Load, pos_symbol_var)
        commands.add(Compare, 0)
        # Если не совпадают, то пропускаем секцию записи результата в переменную
        commands.add(Jz, continue_search_symbol_label)
        commands.add(Store, target_symbol_var)
        commands.add(Load, target_symbol_var)
        commands.add(Label, continue_search_symbol_label)

        # Продолжаем перебирать символы строки
        commands.add(Pop)
        commands.add(Load, counter_var)
        commands.add(Push, 1)
        commands.add(Add)
        commands.add(Store, counter_var)
        commands.add(Jump, start_while_label)

        # Завершаем выполнение цикла, изымаем последнее значение со стека - 0 - маркер начала строки,
        # и помещаем найденный символ на стек (помещается 0, если символа не найдено).
        commands.add(Label, end_while_label)
        commands.add(Pop)
        commands.add(Load, target_symbol_var)

    """
    Генерация инструкций для замены определенного символа строки, находящейся на стеке
    """
    @staticmethod
    def compile_strset(commands, env):
        start_while_label = Environment.create_label(env)
        end_while_label = Environment.create_label(env)
        continue_search_symbol_label = Environment.create_label(env)

        counter_var = Environment.create_var(env)
        pos_symbol_var = Environment.create_var(env)
        replacement_symbol_var = Environment.create_var(env)
        target_symbol_var = Environment.create_var(env)

        # Записываем заменяющий символ (значение из стека) в переменную
        commands.add(Store, replacement_symbol_var)

        # Записываем номер заменяемого символа (значение из стека) в переменную
        commands.add(Store, pos_symbol_var)

        # Инициализиуем счетчик цикла
        commands.add(Push, 0)
        commands.add(Store, counter_var)

        # Запускаем цикл (перебор символов строки)
        commands.add(Label, start_while_label)
        commands.add(Dup)
        commands.add(Jz, end_while_label)
        # Сверяем значение счетчика с нужным номером символа
        commands.add(Load, counter_var)
        commands.add(Load, pos_symbol_var)
        commands.add(Compare, 0)
        # Если не совпадают, то пропускаем секцию записи результата в переменную
        commands.add(Jz, continue_search_symbol_label)
        commands.add(Store, target_symbol_var)
        commands.add(Load, target_symbol_var)
        commands.add(Label, continue_search_symbol_label)

        # Продолжаем перебирать символы строки
        commands.add(Pop)
        commands.add(Load, counter_var)
        commands.add(Push, 1)
        commands.add(Add)
        commands.add(Store, counter_var)
        commands.add(Jump, start_while_label)

        # Завершаем выполнение цикла, изымаем последнее значение со стека - 0 - маркер начала строки,
        # и помещаем найденный символ на стек (помещается 0, если символа не найдено).
        commands.add(Label, end_while_label)
        commands.add(Pop)
        commands.add(Load, target_symbol_var)
