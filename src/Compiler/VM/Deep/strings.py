# -*- coding: utf-8 -*-

from ..Helpers.types import Types
from ..Helpers.base import dbstore, dbload
from ..Helpers.loop import Loop
from ..Helpers.commands import Dup, Store, Push, Mul, DMalloc, Load, Compare, DBStore, Add, DBLoad, Jnz, Label, Jump, Jz, Sub


class StringCompiler:
    @staticmethod
    def store(commands, data):
        """ Генерация инструкций для записи строки из стека в heap memory. """
        str_start_pointer = data.var(Types.INT)
        end_str_pointer = data.var(Types.INT)

        # Добавляем к требуемому размеру памяти 1 - для escape-нуля (маркера конца строки)
        commands.add(Push, 1)
        commands.add(Add)
        commands.add(Dup)
        # Выделяем память размером = числу на стеке (ранее мы записали туда длину строки)
        commands.add(DMalloc, 0)
        commands.add(Dup)
        commands.add(Store, str_start_pointer)
        # Выносим инвариант цикла - указатель на конец строки - в переменную
        commands.add(Add)
        commands.add(Store, end_str_pointer)

        def cycle_body(_counter, b, c):
            # Последовательно сохраняем все символы в выделенной памяти в обратном порядке (т. к. берем со стека)
            dbstore(end_str_pointer, _counter, commands, invert=True, value=-2)

        counter = Loop.stack(commands, data, cycle_body, load_counter=False, return_counter=True)

        # Дописываем 0 в последнюю ячейку памяти - это маркер конца строки
        commands.add(Push, 0)
        dbstore(str_start_pointer, counter, commands)

        # Отдаем на стек указатель на начало строки для дальнейшего использования
        commands.add(Load, str_start_pointer)

    @staticmethod
    def strlen(commands, data, type):
        """ Генерация инструкций для получения длины строки, находящейся на стеке. """
        str_start_pointer = data.var(Types.INT)
        # Разыменовываем лежащий на стеке указатель и записываем его в переменную
        commands.add(Store, str_start_pointer)

        # Считываем строку из памяти до конца (пока не встретим 0), подсчитывая кол-во символов (его кладем на стек)
        Loop.data(commands, data, str_start_pointer, memory_type='heap')

    @staticmethod
    def strget(commands, data, type):
        """ Генерация инструкций для получения определенного символа строки """
        # Прибавляем к номеру ячейки с началом строки номер требуемого символа (offset)
        commands.add(Add)
        # Загружаем на стек символ по номеру его ячейки в heap memory
        commands.add(DBLoad, 0)

    @staticmethod
    def strset(commands, data, type):
        """ Генерация инструкций для замены определенного символа строки """
        # Вычисляем ячейки heap memory, где находится заменяемый символ
        commands.add(Add)
        # Производим замену символа
        commands.add(DBStore, 0)

    @staticmethod
    def strsub(commands, data, type):
        """ Генерация инструкций для получение подстроки строки """
        substr_length = data.var(Types.INT)
        substr_start_pointer = data.var(Types.INT)

        finish_label = data.label()

        # Сохраняем длину подстроки
        commands.add(Store, substr_length)

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

        Loop.data(commands, data, substr_start_pointer, cycle_body, load_counter=False, memory_type='heap')

        commands.add(Label, finish_label)
        # Записываем на стек длину подстроки + 1 (для маркера конца строки - нуля)
        commands.add(Load, substr_length)

        StringCompiler.store(commands, data)

    @staticmethod
    def strdup(commands, data, type):
        """ Генерация инструкций для дублирования строки """
        str_start_pointer = data.var(Types.INT)

        # Разыменовываем лежащий на стеке указатель и записываем его в переменную
        commands.add(Store, str_start_pointer)

        # Кладем на стек 0 - маркер конца строки
        commands.add(Push, 0)

        def cycle_body(_counter, a, b):
            dbload(str_start_pointer, _counter, commands)

        # Читаем строку и кладем её на стек
        Loop.data(commands, data, str_start_pointer, cycle_body, memory_type='heap')

        StringCompiler.store(commands, data)

    @staticmethod
    def strcat_first(commands, data, type):
        """ Генерация инструкций для дублирования первой из конкатенируемых строки """
        str_start_pointer = data.var(Types.INT)

        commands.add(Store, str_start_pointer)
        commands.add(Push, 0)

        def cycle_body(_counter, a, b):
            dbload(str_start_pointer, _counter, commands)

        # Читаем строку и кладем её на стек
        Loop.data(commands, data, str_start_pointer, cycle_body, memory_type='heap')

    @staticmethod
    def strcat_second(commands, data, type):
        """ Генерация инструкций для дублирования второй из конкатенируемых строки и запись её в памяти за первой """
        str_start_pointer = data.var(Types.INT)
        str_length = data.var(Types.INT)

        commands.add(Store, str_start_pointer)
        commands.add(Store, str_length)

        def cycle_body(_counter, a, b):
            dbload(str_start_pointer, _counter, commands)

        # Читаем строку и кладем её на стек
        Loop.data(commands, data, str_start_pointer, cycle_body, memory_type='heap')

        commands.add(Load, str_length)
        commands.add(Add)

        StringCompiler.store(commands, data)

    @staticmethod
    def strmake(commands, data):
        """ Генерация инструкций для создания строки заданной длины с повторяющимся символом """
        str_start_pointer = data.var(Types.INT)
        str_length = data.var(Types.INT)
        basis_symbol = data.var(Types.CHAR)

        finish_label = data.label()

        commands.add(Dup)
        # Сохраняем длину строки в переменную
        commands.add(Store, str_length)
        # Выделяем память = указанной длине строки +1 (плюс маркер конца строки - 0)
        commands.add(DMalloc, 1)
        commands.add(Store, str_start_pointer)
        commands.add(Store, basis_symbol)

        def cycle_body(_counter, b, c):
            commands.add(Load, _counter)
            commands.add(Load, str_length)
            commands.add(Compare, 5)
            commands.add(Jnz, finish_label)
            commands.add(Load, basis_symbol)
            dbstore(str_start_pointer, _counter, commands)

        counter = Loop.simple(commands, data, cycle_body, return_counter=True)

        # Сюда переходим после того, как запишем нужное количество символов в создаваемую строку
        commands.add(Label, finish_label)

        # Дописываем 0 в последнюю ячейку памяти - это маркер конца строки
        commands.add(Push, 0)
        dbstore(str_start_pointer, counter, commands)

        # Отдаем на стек указатель на начало созданной строки для дальнейшего использования
        commands.add(Load, str_start_pointer)

    @staticmethod
    def strcmp(commands, data, type1, type2):
        """ Генерация инструкций для посимвольного сравнивания двух строк """
        str1_start_pointer = data.var(Types.INT)
        str2_start_pointer = data.var(Types.INT)

        eq_label = data.label()
        not_eq_label = data.label()
        finish_label = data.label()

        commands.add(Store, str1_start_pointer)
        commands.add(Store, str2_start_pointer)

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

        counter = Loop.simple(commands, data, cycle_body, return_counter=True)

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
