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

        # Кладем в стек 0 - маркер конца строки
        commands.add(Push, 0)

    """
    Генерация инструкций для записи статической (const) строки из стека в перменную.
    """
    @staticmethod
    def compile_write(commands, env, characters=None):
        for _ in characters:
            commands.add(Store, Environment.create_var(env))

        pointer_start_string = Environment.create_var(env)
        commands.add(Store, pointer_start_string)\
            .add(Push, pointer_start_string)

    """
    Генерация инструкций для динамической записи строки из стека в перменную.
    """
    @staticmethod
    def compile_store(commands, env):
        start_data_pointer = Environment.create_var(env)

        commands.add(DAllocate, 0)
        commands.add(Store, start_data_pointer)

        def cycle_body(counter_var, b, c):
            commands.add(Load, counter_var)
            commands.add(Load, start_data_pointer)
            commands.add(Add)
            commands.add(DBStore, 0)

        counter_var = commands.stack_cycle(env, cycle_body, load_counter=False, return_counter_var=True)
        commands.add(Push, 0)
        commands.add(Load, counter_var)
        commands.add(Load, start_data_pointer)
        commands.add(Add)
        commands.add(DBStore, 0)

        commands.add(Push, start_data_pointer)

    """
    Генерация инструкций для получения длины строки, находящейся на стеке.
    """
    @staticmethod
    def compile_strlen(commands, env, allocate):
        var_number = Environment.create_var(env)

        if allocate == 'heap':
            commands.add(BLoad, 0)
        # Записываем указатель на начало строки в переменную (он лежит на стеке)
        commands.add(Store, var_number)

        # Считываем строку из памяти до конца, подсчитывая кол-во символов
        if allocate == 'heap':
            commands.memory_heap_cycle(env, var_number)
        else:
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

        # Сохраняем заменяющий символ
        commands.add(Store, replacement_symbol_var)

        # Вычисляем и сохраняем адрес ячейки памяти, где находится заменяемый символ
        commands.add(Sub)
        commands.add(Store, position_symbol_var)

        # Загружаем на стек адрес и сам символ в нужном порядке
        commands.add(Load, replacement_symbol_var)
        commands.add(Load, position_symbol_var)

        # Выгружаем символ со стека в ячейку памяти по вычисленному адресу
        commands.add(BStore, 0)

    """
    Генерация инструкций для получение подстроки строки
    """
    @staticmethod
    def compile_strsub(commands, env):
        length_var = Environment.create_var(env)
        string_var = Environment.create_var(env)

        end_label = Environment.create_label(env)

        # Сохраняем заменяющий символ
        commands.add(Store, length_var)
        commands.add(Add)
        # Вычисляем и сохраняем адрес ячейки памяти, где находится заменяемый символ
        commands.add(Store, string_var)

        commands.add(Push, 0)

        def cycle_body(counter_var, a, b):
            commands.add(Load, counter_var)
            commands.add(Load, length_var)
            commands.add(Compare, 5)
            commands.add(Jnz, end_label)
            commands.add(Load, string_var)
            commands.add(Load, counter_var)
            commands.add(Sub)
            commands.add(BLoad, 0)

        counter_var = commands.memory_cycle(env, string_var, cycle_body, return_counter_var=True)

        commands.add(Label, end_label)
        commands.add(Load, counter_var)
        commands.add(Push, 1)
        commands.add(Add)
