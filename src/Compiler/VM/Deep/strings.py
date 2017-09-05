# -*- coding: utf-8 -*-

from ..Helpers.base import *
from ..Helpers.loop import Loop

class StringCompiler:
    """
    Генерация инструкций для записи строки из стека в heap memory.
    """
    @staticmethod
    def store(commands, env):
        str_start_pointer = env.var()
        end_str_pointer = env.var()

        # Добавляем к требуемому размеру памяти 1 - для escape-нуля (маркера конца строки)
        commands.add(Push, 1)
        commands.add(Add)
        commands.add(Dup)
        # Выделяем память размером = числу на стеке (ранее мы записали туда длину строки)
        commands.add(DAllocate, 0)
        commands.add(Dup)
        commands.add(Store, str_start_pointer)
        # Выносим инвариант цикла - указатель на конец строки - в переменную
        commands.add(Add)
        commands.add(Store, end_str_pointer)

        def cycle_body(_counter, b, c):
            # Последовательно сохраняем все символы в выделенной памяти в обратном порядке (т. к. берем со стека)
            dbstore(end_str_pointer, _counter, commands, invert=True, value=-2)

        counter = Loop.stack(commands, env, cycle_body, load_counter=False, return_counter=True)

        # Дописываем 0 в последнюю ячейку памяти - это маркер конца строки
        commands.add(Push, 0)
        dbstore(str_start_pointer, counter, commands)

        # Отдаем на стек указатель на начало строки для дальнейшего использования
        commands.add(Push, str_start_pointer)

    """
    Генерация инструкций для получения длины строки, находящейся на стеке.
    """
    @staticmethod
    def strlen(commands, env):
        str_start_pointer = env.var()

        # Разыменовываем лежащий на стеке указатель и записываем его в переменную
        bload_and_store(str_start_pointer, commands)

        # Считываем строку из памяти до конца (пока не встретим 0), подсчитывая кол-во символов (его кладем на стек)
        Loop.data_heap(commands, env, str_start_pointer)

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
            # Загружаем очередной символ подстроки из heap memory
            dbload(substr_start_pointer, _counter, commands)

        Loop.data_heap(commands, env, substr_start_pointer, cycle_body, load_counter=False)

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

        # Разыменовываем лежащий на стеке указатель и записываем его в переменную
        bload_and_store(str_start_pointer, commands)

        # Кладем на стек 0 - маркер конца строки
        commands.add(Push, 0)

        def cycle_body(_counter, a, b):
            dbload(str_start_pointer, _counter, commands)

        # Читаем строку и кладем её на стек
        Loop.data_heap(commands, env, str_start_pointer, cycle_body)

        StringCompiler.store(commands, env)

    """
    Генерация инструкций для дублирования первой из конкатенируемых строки
    """
    @staticmethod
    def strcat_first(commands, env):
        str_start_pointer = env.var()

        bload_and_store(str_start_pointer, commands)
        commands.add(Push, 0)

        def cycle_body(_counter, a, b):
            dbload(str_start_pointer, _counter, commands)

        # Читаем строку и кладем её на стек
        Loop.data_heap(commands, env, str_start_pointer, cycle_body)

    """
    Генерация инструкций для дублирования второй из конкатенируемых строки и запись её в памяти за первой
    """
    @staticmethod
    def strcat_second(commands, env):
        str_start_pointer = env.var()
        str_length = env.var()

        bload_and_store(str_start_pointer, commands)
        commands.add(Store, str_length)

        def cycle_body(_counter, a, b):
            dbload(str_start_pointer, _counter, commands)

        # Читаем строку и кладем её на стек
        Loop.data_heap(commands, env, str_start_pointer, cycle_body)

        commands.add(Load, str_length)
        commands.add(Add)

        StringCompiler.store(commands, env)

    """
    Генерация инструкций для создания строки заданной длины с повторяющимся символом
    """
    @staticmethod
    def strmake(commands, env):
        str_start_pointer = env.var()
        str_length = env.var()
        basis_symbol = env.var()

        finish_label = env.label()

        commands.add(Dup)
        # Сохраняем длину строки в переменную
        commands.add(Store, str_length)
        # Выделяем память = указанной длине строки +1 (плюс маркер конца строки - 0)
        commands.add(DAllocate, 1)
        commands.add(Store, str_start_pointer)
        commands.add(Store, basis_symbol)

        def cycle_body(_counter, b, c):
            commands.add(Load, _counter)
            commands.add(Load, str_length)
            commands.add(Compare, 5)
            commands.add(Jnz, finish_label)
            commands.add(Load, basis_symbol)
            dbstore(str_start_pointer, _counter, commands)

        counter = Loop.simple(commands, env, cycle_body, return_counter=True)

        # Сюда переходим после того, как запишем нужное количество символов в создаваемую строку
        commands.add(Label, finish_label)

        # Дописываем 0 в последнюю ячейку памяти - это маркер конца строки
        commands.add(Push, 0)
        dbstore(str_start_pointer, counter, commands)

        # Отдаем на стек указатель на начало созданной строки для дальнейшего использования
        commands.add(Push, str_start_pointer)

    """
    Генерация инструкций для посимвольного сравнивания двух строк
    """
    @staticmethod
    def strcmp(commands, env):
        str1_start_pointer = env.var()
        str2_start_pointer = env.var()

        eq_label = env.label()
        not_eq_label = env.label()
        finish_label = env.label()

        bload_and_store(str1_start_pointer, commands)
        bload_and_store(str2_start_pointer, commands)

        def cycle_body(_counter, a, continue_label):
            # Загружаем n-ный символ 1-й строки
            dbload(str1_start_pointer, _counter, commands)
            # Дублируем на стек для дальнейшей проверки (чтобы не загружать снова)
            commands.add(Dup)
            # Загружаем n-ный символ 2-й строки
            dbload(str2_start_pointer, _counter, commands)
            commands.add(Compare, 1)
            # Если символы не равны, сразу переходим в секцию not_eq_label и выясняем уже там - какой из них больше
            # Это также работает, когда мы достиги конца одной из строк (какой-то символ и 0)
            commands.add(Jnz, not_eq_label)

            commands.add(Push, 0)
            # Сравниваем с 0 ранее продублированный символ (1-й строки) - если он равен нулю, то равен и второй,
            # т. к. в эту секцию мы попадаем только при равенстве обоих символов
            commands.add(Compare, 0)
            # 0 говорит о достижении конца строки - если это не 0, то продолжаем цикл
            commands.add(Jz, continue_label)
            # Сюда попадаем, когда достигли конца одновременно двух строк - т. е. они полностью равны
            commands.add(Jump, eq_label)

        counter = Loop.simple(commands, env, cycle_body, return_counter=True)

        # Секция полного равенства строк: пишем на стек 0
        commands.add(Label, eq_label)
        commands.add(Push, 0)
        commands.add(Jump, finish_label)

        # Секция неравенства строк
        commands.add(Label, not_eq_label)
        # Загружаем только второй символ - первый у нас уже содержится на стеке (см. тело цикла)
        dbload(str2_start_pointer, counter, commands)
        # Сравниваем символы оператором <
        commands.add(Compare, 2)
        # Производим нормировку результата сравнения: 0|1 -> -1|1
        commands.add(Push, 2)
        commands.add(Mul)
        commands.add(Push, 1)
        commands.add(Sub)

        commands.add(Label, finish_label)
