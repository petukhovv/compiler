# -*- coding: utf-8 -*-

from src.VM.commands import *
from environment import Environment

class String:
    """
    Генерация инструкций для загрузки строки из переменной в стек.
    """
    @staticmethod
    def compile_load(commands, env, var_number):
        end_label = Environment.create_label(env)

        # Кладем в стек 0 - маркер конца строки.
        commands.add(Push, 0)

        # Если строка пустая (т. е. var_number - пустой указатель, т. е. равен 0), пропускаем цикл и сразу выходим.
        commands.add(Load, var_number)\
            .add(Jz, end_label)

        def cycle_body(counter_var, a, b):
            commands.add(Load, var_number)\
                .add(Load, counter_var)\
                .add(Add)
            # Загружаем очередной символ строки в стек по номеру переменной, хранящейся на стеке.
            # Номер вычисляется как номер переменной + текущее значение счетчика.
            commands.add(BLoad, 0)

        commands.cycle(env, cycle_body, load_counter=False)\
            .add(Label, end_label)

    """
    Генерация инструкций для записи статической (const) строки из стека в перменную.
    """
    @staticmethod
    def compile_write(commands, env, characters=None):
        pointer_start_string = 0

        for char in characters:
            var_number = Environment.create_var(env)
            if pointer_start_string == 0:
                pointer_start_string = var_number
            commands.add(Store, var_number)

        commands.add(Store, Environment.create_var(env))\
            .add(Push, pointer_start_string)

    """
    Генерация инструкций для получения длины строки, находящейся на стеке.
    """
    @staticmethod
    def compile_strlen(commands, env):
        end_label = Environment.create_label(env)

        # Если строка пустая (т. е. на стеке 0 - маркер конца строки), пропускаем цикл и сразу выходим.
        commands.add(Dup)\
            .add(Jz, end_label)

        commands.cycle(env, lambda a, b, c: commands.add(Pop))\
            .add(Label, end_label)

    """
    Генерация инструкций для получения определенного символа строки, находящейся на стеке
    """
    @staticmethod
    def compile_strget(commands, env):
        continue_search_symbol_label = Environment.create_label(env)
        pos_symbol_var = Environment.create_var(env)
        target_symbol_var = Environment.create_var(env)

        # Записываем значение из стека в переменную (это номер позиции нужного символа)
        commands.add(Store, pos_symbol_var)

        def cycle_body(counter_var, break_label, c):
            # Сверяем значение счетчика с нужным номером символа
            commands.add(Load, counter_var)\
                .add(Load, pos_symbol_var)\
                .add(Compare, 0)
            # Если не совпадают, то пропускаем секцию записи результата в переменную,
            # если совпадают - записывает текущий символ в переменную и выходим из цикла.
            commands.add(Jz, continue_search_symbol_label)\
                .add(Store, target_symbol_var)\
                .add(Load, target_symbol_var)\
                .add(Jump, break_label)\
                .add(Label, continue_search_symbol_label)\
                .add(Pop)

        # Ищем нужный символ
        commands.cycle(env, cycle_body)

        # Удаляем из стека оставшуюся часть строки
        commands.cycle(env, lambda a, b, c: commands.add(Pop))

        # Помещаем найденный символ на стек (помещается 0, если символа не найдено).
        commands.add(Load, target_symbol_var)

    """
    Генерация инструкций для замены определенного символа строки, находящейся на стеке
    """
    @staticmethod
    def compile_strset(commands, env):
        continue_search_symbol_label = Environment.create_label(env)

        pos_symbol_var = Environment.create_var(env)

        new_symbol_var = Environment.create_var(env)
        target_symbol_var = Environment.create_var(env)

        # Буфер (указатель на начало строки) для записи прочитанной части строки
        buffer = Environment.create_var(env)

        # Записываем значение из стека в переменную (это заменяющий символ)
        commands.add(Store, new_symbol_var)

        # Записываем значение из стека в переменную (это номер позиции заменяемого символа)
        commands.add(Store, pos_symbol_var)

        def cycle_body(counter_var, a, b):
            # Сверяем значение счетчика с нужным номером символа
            commands.add(Load, counter_var) \
                .add(Load, pos_symbol_var) \
                .add(Compare, 0)
            # Если не совпадают, то пропускаем секцию записи результата в переменную
            commands.add(Jz, continue_search_symbol_label) \
                .add(Store, target_symbol_var) \
                .add(Load, target_symbol_var) \
                .add(Label, continue_search_symbol_label) \
                .add(Pop)

        commands.cycle(env, cycle_body)

        # Помещаем найденный символ на стек (помещается 0, если символа не найдено).
        commands.add(Load, target_symbol_var)
