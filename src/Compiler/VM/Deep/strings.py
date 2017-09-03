# -*- coding: utf-8 -*-

from src.VM.commands import *

class StringCompiler:
    """
    Генерация инструкций для записи строки из стека в heap memory.
    """
    @staticmethod
    def store(commands, env):
        start_str_pointer = env.var()
        end_str_pointer = env.var()

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
        str_start_pointer = env.var()

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
        # Получаем номер ячейки в heap memory с началом строки
        commands.add(BLoad, 0)
        # Прибавляем к номеру ячейки с началом строки номер требуемого символа (offset)
        commands.add(Add)
        # Загружаем на стек символ по номеру его ячейки в heap memory
        commands.add(DBLoad, 0)

    """
    Генерация инструкций для замены определенного символа строки
    """
    @staticmethod
    def strset(commands, env):
        # Получаем номер ячейки в heap memory с началом строки
        commands.add(BLoad, 0)
        # Вычисляем ячейки heap memory, где находится заменяемый символ
        commands.add(Add)
        # Производим замену символа
        commands.add(DBStore, 0)

    """
    Генерация инструкций для получение подстроки строки
    """
    @staticmethod
    def strsub(commands, env):
        substr_length = env.var()
        substr_start_pointer = env.var()

        finish_label = env.label()

        # Сохраняем длину подстроки
        commands.add(Store, substr_length)

        # Вычисляем и сохраняем указатель на начало подстроки
        commands.add(BLoad, 0)
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

        StringCompiler.store(commands, env)

    """
    Генерация инструкций для дублирования строки
    """
    @staticmethod
    def strdup(commands, env):
        str_start_pointer = env.var()

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

        StringCompiler.store(commands, env)

    """
    Генерация инструкций для дублирования строки
    """
    @staticmethod
    def strcat(commands, env):
        str_start_pointer = env.var()

        commands.add(BLoad, 0)
        commands.add(Store, str_start_pointer)

        commands.add(Push, 0)

        def cycle_body(_counter, a, b):
            commands.add(Load, str_start_pointer)
            commands.add(Load, _counter)
            commands.add(Add)
            commands.add(DBLoad, 0)

        # Читаем строку и кладем её на стек
        commands.loop_data_heap(env, str_start_pointer, cycle_body)

    @staticmethod
    def strcat_join(commands, env):
        str_start_pointer = env.var()
        str_length = env.var()

        commands.add(BLoad, 0)
        commands.add(Store, str_start_pointer)
        commands.add(Store, str_length)

        def cycle_body(_counter, a, b):
            commands.add(Load, str_start_pointer)
            commands.add(Load, _counter)
            commands.add(Add)
            commands.add(DBLoad, 0)

        # Читаем строку и кладем её на стек
        commands.loop_data_heap(env, str_start_pointer, cycle_body)

        commands.add(Load, str_length)
        commands.add(Add)

        StringCompiler.store(commands, env)

    @staticmethod
    def strmake(commands, env):
        str_start_pointer = env.var()
        str_length = env.var()
        basis_symbol = env.var()

        finish_label = env.label()

        commands.add(Dup)
        commands.add(Store, str_length)
        commands.add(DAllocate, 1)
        commands.add(Store, str_start_pointer)

        commands.add(Store, basis_symbol)

        def cycle_body(_counter, b, c):
            commands.add(Load, _counter)
            commands.add(Load, str_length)
            commands.add(Compare, 5)
            commands.add(Jnz, finish_label)
            commands.add(Load, basis_symbol)
            commands.add(Load, str_start_pointer)
            commands.add(Load, _counter)
            commands.add(Add)
            commands.add(DBStore, 0)

        counter = commands.loop(env, cycle_body, return_counter=True)

        commands.add(Label, finish_label)

        # Дописываем 0 в последнюю ячейку памяти - это маркер конца строки
        commands.add(Push, 0)
        commands.add(Load, counter)
        commands.add(Load, str_start_pointer)
        commands.add(Add)
        commands.add(DBStore, 0)

        # Отдаем на стек указатель на начало строки для дальнейшего использования
        commands.add(Push, str_start_pointer)

    @staticmethod
    def strcmp(commands, env):
        str1_start_pointer = env.var()
        str2_start_pointer = env.var()
        str1_symbol = env.var()
        str2_symbol = env.var()

        finish_label = env.label()
        not_eq_label = env.label()
        eq_label = env.label()
        larger_label = env.label()
        smaller_label = env.label()
        continue_label = env.label()

        commands.add(BLoad, 0)
        commands.add(Store, str1_start_pointer)

        commands.add(BLoad, 0)
        commands.add(Store, str2_start_pointer)

        def cycle_body(_counter, a, _):
            commands.add(Load, str1_start_pointer)
            commands.add(Load, _counter)
            commands.add(Add)
            commands.add(DBLoad, 0)
            commands.add(Store, str1_symbol)

            commands.add(Load, str2_start_pointer)
            commands.add(Load, _counter)
            commands.add(Add)
            commands.add(DBLoad, 0)
            commands.add(Store, str2_symbol)

            commands.add(Load, str1_symbol)
            commands.add(Load, str2_symbol)
            commands.add(Compare, 1)
            commands.add(Jnz, not_eq_label)

            commands.add(Load, str1_symbol)
            commands.add(Push, 0)
            commands.add(Compare, 0)
            commands.add(Load, str2_symbol)
            commands.add(Push, 0)
            commands.add(Compare, 0)
            commands.add(Push, 1)
            commands.add(Compare, 0)
            commands.add(Dup)
            commands.add(Jz, continue_label)
            commands.add(Compare, 0)
            commands.add(Jnz, eq_label)

            commands.add(Label, continue_label)
            commands.add(Pop)
            commands.add(Pop)

        # Читаем строку и кладем её на стек
        counter = commands.loop(env, cycle_body, return_counter=True)

        commands.add(Label, eq_label)
        commands.add(Push, 0)
        commands.add(Jump, finish_label)

        commands.add(Label, not_eq_label)

        commands.add(Load, str1_start_pointer)
        commands.add(Load, counter)
        commands.add(Add)
        commands.add(DBLoad, 0)

        commands.add(Load, str2_start_pointer)
        commands.add(Load, counter)
        commands.add(Add)
        commands.add(DBLoad, 0)

        commands.add(Compare, 2)
        commands.add(Jnz, larger_label)

        commands.add(Push, -1)
        commands.add(Jump, finish_label)

        commands.add(Label, larger_label)
        commands.add(Push, 1)
        commands.add(Jump, finish_label)

        commands.add(Label, finish_label)
