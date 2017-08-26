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

        commands.stack_cycle(env, cycle_body, load_counter=False)\
            .add(Label, end_label)

        # Кладем в стек 0 - маркер конца строки.
        commands.add(Push, 0)

    """
    Генерация инструкций для записи статической (const) строки из стека в перменную.
    """
    @staticmethod
    def compile_write(commands, env, characters=None):
        for char in characters:
            commands.add(Store, Environment.create_var(env))

        pointer_start_string = Environment.create_var(env)
        commands.add(Store, pointer_start_string)\
            .add(Push, pointer_start_string)

    """
    Генерация инструкций для получения длины строки, находящейся на стеке.
    """
    @staticmethod
    def compile_strlen(commands, env):
        var_number = Environment.create_var(env)

        # Записываем указатель на начало строки в переменную (он лежит на стеке)
        commands.add(Store, var_number)

        # Считываем строку из памяти до конца, подсчитывая кол-во символов
        commands.memory_cycle(env, var_number)

    """
    Генерация инструкций для получения определенного символа строки, находящейся на стеке
    """
    @staticmethod
    def compile_strget(commands, env):
        # Вычитаем из указателя на начало строки номер нужного символа (т. к. в памяти строка инвертирована)
        commands.add(Sub)
        # Загружаем символ по вычисленному адресу
        commands.add(BLoad, 0)

    """
    Генерация инструкций для замены определенного символа строки, находящейся на стеке
    """
    @staticmethod
    def compile_strset(commands, env):
        replacement_symbol_var = Environment.create_var(env)
        position_symbol_var = Environment.create_var(env)

        # Запоминаем заменяющий символ
        commands.add(Store, replacement_symbol_var)

        # Вычисляем адрес ячейки памяти, где находится заменяемый символ
        commands.add(Sub)
        commands.add(Store, position_symbol_var)

        # Загружаем на стек адрес и сам символ в нужном порядке
        commands.add(Load, replacement_symbol_var)
        commands.add(Load, position_symbol_var)

        # Выгружаем символ со стека в ячейку памяти по вычисленному адресу
        commands.add(BStore, 0)
