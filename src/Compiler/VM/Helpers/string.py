# -*- coding: utf-8 -*-

from src.VM.commands import *
from env import Env

class String:
    """
    Генерация инструкций для записи строки из стека в heap memory.
    """
    @staticmethod
    def _store(commands, env):
        start_str_pointer = Env.var(env)
        end_str_pointer = Env.var(env)

        # Добавляем к требуемому размеру памяти 1 - для escape-нуля (маркера конца строки)
        commands.add(Push, 1)
        commands.add(Add)
        commands.add(Dup)
        # Выделяем память размером = числу на стеке (ранее мы записали туда длину строки)
        commands.add(DAllocate, 0)
        commands.add(Store, start_str_pointer)
        # Выносим инвариант цикла - указатель на конец строки - в переменную
        commands.add(Load, start_str_pointer)
        commands.add(Add)
        commands.add(Store, end_str_pointer)

        def cycle_body(_counter, b, c):
            commands.add(Load, end_str_pointer)
            commands.add(Load, _counter)
            commands.add(Sub)
            commands.add(DBStore, -2)

        counter = commands.loop_stack(env, cycle_body, load_counter=False, return_counter=True)

        # Дописываем 0 в последнюю ячейку памяти - это маркер конца строки
        commands.add(Push, 0)
        commands.add(Load, counter)
        commands.add(Load, start_str_pointer)
        commands.add(Add)
        commands.add(DBStore, 0)

        # Отдаем на стек указатель на начало строки для дальнейшего использования
        commands.add(Push, start_str_pointer)

    """
    Генерация инструкций для получения длины строки, находящейся на стеке.
    """
    @staticmethod
    def strlen(commands, env):
        str_start_pointer = Env.var(env)

        commands.add(BLoad, 0)
        # Записываем указатель на начало строки в переменную (он лежит на стеке)
        commands.add(Store, str_start_pointer)

        # Считываем строку из памяти до конца (пока не встретим 0), подсчитывая кол-во символов (его кладем на стек)
        commands.loop_data_heap(env, str_start_pointer)

    """
    Генерация инструкций для получения определенного символа строки
    """
    @staticmethod
    def strget(commands, env):
        target_symbol = Env.var(env)

        commands.add(Store, target_symbol)
        # Получаем номер ячейки в heap memory с началом строки
        commands.add(BLoad, 0)
        commands.add(Load, target_symbol)
        # Прибавляем к номеру ячейки с началом строки номер требуемого символа (offset)
        commands.add(Add)
        # Загружаем на стек символ по номеру его ячейки в heap memory
        commands.add(DBLoad, 0)

    """
    Генерация инструкций для замены определенного символа строки
    """
    @staticmethod
    def strset(commands, env):
        replacement_symbol = Env.var(env)
        target_symbol = Env.var(env)
        target_symbol_pointer = Env.var(env)

        # Сохраняем заменяющий символ
        commands.add(Store, replacement_symbol)

        # Сохраняем номер заменяемого символа
        commands.add(Store, target_symbol)
        commands.add(BLoad, 0)
        commands.add(Load, target_symbol)
        # Вычисляем и сохраняем адрес ячейки heap memory, где находится заменяемый символ
        commands.add(Add)
        commands.add(Store, target_symbol_pointer)
        # Загружаем в нужном порядке: заменяющий символ и указатель на заменяемый символ
        commands.add(Load, replacement_symbol)
        commands.add(Load, target_symbol_pointer)

        # Производим замену символа
        commands.add(DBStore, 0)

    """
    Генерация инструкций для получение подстроки строки
    """
    @staticmethod
    def strsub(commands, env):
        substr_offset = Env.var(env)
        substr_length = Env.var(env)
        substr_start_pointer = Env.var(env)

        finish_label = Env.label(env)

        # Сохраняем длину подстроки
        commands.add(Store, substr_length)

        # Сохраняем смещение относительно строки
        commands.add(Store, substr_offset)
        # Вычисляем и сохраняем указатель на начало подстроки
        commands.add(BLoad, 0)
        commands.add(Load, substr_offset)
        commands.add(Add)
        commands.add(Store, substr_start_pointer)

        # Кладем на стек 0 - маркер конца строки
        commands.add(Push, 0)

        def cycle_body(_counter, a, b):
            commands.add(Load, _counter)
            commands.add(Load, substr_length)
            commands.add(Compare, 5)
            # Если уже прочитали и записали подстркоу требуемой длины - выходим из цикла
            commands.add(Jnz, finish_label)
            # Вычисляем и загружаем очередной символ подстроки
            commands.add(Load, substr_start_pointer)
            commands.add(Load, _counter)
            commands.add(Add)
            commands.add(DBLoad, 0)

        commands.loop_data_heap(env, substr_start_pointer, cycle_body, load_counter=False)

        commands.add(Label, finish_label)
        # Записываем на стек длину подстроки + 1 (для маркера конца строки - нуля)
        commands.add(Load, substr_length)

    """
    Генерация инструкций для дублирования строки
    """
    @staticmethod
    def strdup(commands, env):
        str_start_pointer = Env.var(env)

        # Разыменовываем указатель на начало строки
        commands.add(BLoad, 0)
        # Записываем номер первого символа строки в переменную (он лежит на стеке)
        commands.add(Store, str_start_pointer)

        # Кладем на стек 0 - маркер конца строки
        commands.add(Push, 0)

        def cycle_body(_counter, a, b):
            commands.add(Load, str_start_pointer)
            commands.add(Load, _counter)
            commands.add(Add)
            commands.add(DBLoad, 0)

        # Читаем строку и кладем её на стек
        commands.loop_data_heap(env, str_start_pointer, cycle_body)
