from ..Helpers.base import *
from ..Helpers.loop import Loop
from ..Core.registers import Registers
from ..Utils.malloc import Malloc


class StringCompiler:
    @staticmethod
    def store(compiler):
        """ Генерация инструкций для записи строки из стека в heap memory. """
        str_start_pointer = compiler.environment.add_local_var(Types.INT)
        end_str_pointer = compiler.environment.add_local_var(Types.INT)

        # Добавляем к требуемому размеру памяти 1 - для escape-нуля (маркера конца строки)
        compiler.code.add(Commands.POP, Registers.EAX)\
            .add(Commands.ADD, [Registers.EAX, 1])\
            .add(Commands.PUSH, Registers.EAX)\
            .add(Commands.PUSH, Registers.EAX)
        # Выделяем память размером = числу на стеке (ранее мы записали туда длину строки)
        Malloc(compiler).call()
        compiler.code.add(Commands.MOV, [str_start_pointer, Registers.EAX])

        # Выносим инвариант цикла - указатель на конец строки - в переменную
        compiler.code.add(Commands.POP, Registers.EBX)\
            .add(Commands.ADD, [Registers.EAX, Registers.EBX])\
            .add(Commands.MOV, [end_str_pointer, Registers.EAX])

        def cycle_body(_counter, b, c):
            # Последовательно сохраняем все символы в выделенной памяти в обратном порядке (т. к. берем со стека)
            dbstore(compiler, end_str_pointer, _counter, invert=True, value=-2)

        counter = Loop.stack(compiler, cycle_body, load_counter=False, return_counter=True)

        # Дописываем 0 в последнюю ячейку памяти - это маркер конца строки
        compiler.code.add(Commands.PUSH, 0)
        dbstore(compiler, str_start_pointer, counter)

        # Отдаем на стек указатель на начало строки для дальнейшего использования
        compiler.code.add(Commands.PUSH, str_start_pointer)

    @staticmethod
    def strlen(compiler):
        """ Генерация инструкций для получения длины строки, находящейся на стеке. """
        str_start_pointer = compiler.environment.add_local_var(Types.INT)

        # Разыменовываем лежащий на стеке указатель и записываем его в переменную
        compiler.code.add(Commands.POP, str_start_pointer)

        # Считываем строку из памяти до конца (пока не встретим 0), подсчитывая кол-во символов (его кладем на стек)
        Loop.data(compiler, str_start_pointer)

    @staticmethod
    def strget(compiler, type):
        """ Генерация инструкций для получения определенного символа строки """
        # Прибавляем к номеру ячейки с началом строки номер требуемого символа (offset)
        compiler.code.add(Commands.POP, Registers.EAX)\
            .add(Commands.POP, Registers.EBX)\
            .add(Commands.ADD, [Registers.EAX, Registers.EBX])
        # Загружаем на стек символ по номеру его ячейки в heap memory
        compiler.code.add(Commands.MOVZX, [Registers.EBX, 'byte [%s]' % Registers.EAX])\
            .add(Commands.PUSH, Registers.EBX)

    @staticmethod
    def strset(compiler, type):
        """ Генерация инструкций для замены определенного символа строки """
        # Вычисляем ячейки heap memory, где находится заменяемый символ
        compiler.code.add(Commands.POP, Registers.EAX)\
            .add(Commands.POP, Registers.EBX)\
            .add(Commands.ADD, [Registers.EAX, Registers.EBX])\
            .add(Commands.POP, Registers.EBX)

        # Производим замену символа
        compiler.code.add(Commands.MOV, ['byte [%s]' % Registers.EAX, Registers.BL])

    @staticmethod
    def strsub(compiler, type):
        """ Генерация инструкций для получение подстроки строки """
        substr_length = compiler.environment.add_local_var(Types.INT)
        substr_start_pointer = compiler.environment.add_local_var(Types.INT)
        start_substr_pointer = compiler.environment.add_local_var(Types.INT)
        end_substr_pointer = compiler.environment.add_local_var(Types.INT)

        finish_label = compiler.labels.create()

        # Сохраняем длину подстроки
        compiler.code.add(Commands.POP, substr_length)

        # Сохраняем указатель на начало подстроки
        compiler.code.add(Commands.POP, Registers.EAX)\
            .add(Commands.POP, Registers.EBX)\
            .add(Commands.ADD, [Registers.EAX, Registers.EBX])\
            .add(Commands.MOV, [substr_start_pointer, Registers.EAX])

        # Выделяем память размером = длине подстроки + 1 (для escape нуля)
        compiler.code.add(Commands.MOV, [Registers.EAX, substr_length])\
            .add(Commands.ADD, [Registers.EAX, 1])
        Malloc(compiler).call()
        compiler.code.add(Commands.MOV, [start_substr_pointer, Registers.EAX])

        # Сохраняем указатель на конец подстроки
        compiler.code.add(Commands.MOV, [Registers.EAX, substr_length])\
            .add(Commands.MOV, [Registers.EBX, start_substr_pointer])\
            .add(Commands.ADD, [Registers.EAX, Registers.EBX])\
            .add(Commands.MOV, [end_substr_pointer, Registers.EAX])

        # Кладем на стек 0 - маркер конца строки
        compiler.code.add(Commands.PUSH, 0)
        dbstore(compiler, end_substr_pointer, None)

        def cycle_body(_counter, a, b):
            compiler.code.add(Commands.MOV, [Registers.EAX, _counter])\
                .add(Commands.MOV, [Registers.EBX, substr_length])\
                .add(Commands.CMP, [Registers.EAX, Registers.EBX])
            # Если уже прочитали и записали подстркоу требуемой длины - выходим из цикла
            compiler.code.add(Commands.JZ, finish_label)
            # Загружаем очередной символ подстроки из heap memory
            dbload(compiler, substr_start_pointer, _counter)
            dbstore(compiler, start_substr_pointer, _counter)

        Loop.data(compiler, substr_start_pointer, cycle_body, load_counter=False)

        compiler.code.add_label(finish_label)
        # Отдаем на стек указатель на начало подстроки для дальнейшего использования
        compiler.code.add(Commands.PUSH, start_substr_pointer)

    @staticmethod
    def strdup(compiler, type):
        """ Генерация инструкций для дублирования строки """
        substr_length = compiler.environment.add_local_var(Types.INT)
        str_start_pointer = compiler.environment.add_local_var(Types.INT)
        new_str_start_pointer = compiler.environment.add_local_var(Types.INT)
        new_end_str_pointer = compiler.environment.add_local_var(Types.INT)

        # Разыменовываем лежащий на стеке указатель и записываем его в переменную
        compiler.code.add(Commands.POP, str_start_pointer)

        # Считываем строку из памяти до конца (пока не встретим 0), подсчитывая кол-во символов (его кладем на стек)
        Loop.data(compiler, str_start_pointer)
        compiler.code.add(Commands.POP, Registers.EAX)\
            .add(Commands.MOV, [substr_length, Registers.EAX])
        Malloc(compiler).call()
        compiler.code.add(Commands.MOV, [new_str_start_pointer, Registers.EAX])

        # Сохраняем указатель на конец новой строки
        compiler.code.add(Commands.MOV, [Registers.EAX, substr_length])\
            .add(Commands.MOV, [Registers.EBX, new_str_start_pointer])\
            .add(Commands.ADD, [Registers.EAX, Registers.EBX])\
            .add(Commands.MOV, [new_end_str_pointer, Registers.EAX])

        # Кладем на стек 0 - маркер конца строки
        compiler.code.add(Commands.PUSH, 0)
        dbstore(compiler, new_end_str_pointer, None)

        def cycle_body(_counter, a, b):
            dbload(compiler, str_start_pointer, _counter)
            dbstore(compiler, new_str_start_pointer, _counter)

        # Читаем строку и кладем её на стек
        Loop.data(compiler, str_start_pointer, cycle_body, load_counter=False)

        # Отдаем на стек указатель на начало подстроки для дальнейшего использования
        compiler.code.add(Commands.PUSH, new_str_start_pointer)

    @staticmethod
    def strcat_calc_length(compiler):
        compiler.code.add(Commands.POP, Registers.EAX)\
            .add(Commands.POP, Registers.EBX)\
            .add(Commands.PUSH, Registers.EAX)\
            .add(Commands.PUSH, Registers.EBX)\
            .add(Commands.PUSH, Registers.EAX)\
            .add(Commands.PUSH, Registers.EBX)

        StringCompiler.strlen(compiler)
        compiler.code.add(Commands.POP, Registers.EAX)\
            .add(Commands.POP, Registers.EBX)\
            .add(Commands.PUSH, Registers.EAX)\
            .add(Commands.PUSH, Registers.EBX)
        StringCompiler.strlen(compiler)
        compiler.code.add(Commands.POP, Registers.EAX)\
            .add(Commands.POP, Registers.EBX)\
            .add(Commands.ADD, [Registers.EAX, Registers.EBX])\
            .add(Commands.PUSH, Registers.EAX)

    @staticmethod
    def strcat(compiler):
        """ Генерация инструкций для дублирования первой из конкатенируемых строки """
        str_length = compiler.environment.add_local_var(Types.INT)
        new_str_start_pointer = compiler.environment.add_local_var(Types.INT)
        new_end_str_pointer = compiler.environment.add_local_var(Types.INT)
        str1_start_pointer = compiler.environment.add_local_var(Types.INT)
        str2_start_pointer = compiler.environment.add_local_var(Types.INT)
        counter_with_offset = compiler.environment.add_local_var(Types.INT)

        compiler.code.add(Commands.POP, Registers.EAX)\
            .add(Commands.ADD, [Registers.EAX, 1])\
            .add(Commands.POP, str1_start_pointer)\
            .add(Commands.POP, str2_start_pointer)\
            .add(Commands.MOV, [str_length, Registers.EAX])
        Malloc(compiler).call()

        # Разыменовываем лежащий на стеке указатель и записываем его в переменную
        compiler.code.add(Commands.MOV, [new_str_start_pointer, Registers.EAX])\
            .add(Commands.MOV, [Registers.EBX, str_length])\
            .add(Commands.ADD, [Registers.EAX, Registers.EBX])\
            .add(Commands.MOV, [new_end_str_pointer, Registers.EAX])

        compiler.code.add(Commands.PUSH, 0)
        dbstore(compiler, new_end_str_pointer, None)

        def cycle_body(str_start_pointer, _counter, offset=None):
            dbload(compiler, str_start_pointer, _counter)
            if offset:
                compiler.code.add(Commands.MOV, [Registers.EAX, _counter])\
                    .add(Commands.MOV, [Registers.EBX, offset])\
                    .add(Commands.ADD, [Registers.EAX, Registers.EBX])\
                    .add(Commands.MOV, [counter_with_offset, Registers.EAX])
            dbstore(compiler, new_str_start_pointer, counter_with_offset if offset else _counter)

        # Читаем строку и кладем её на стек
        counter = Loop.data(
            compiler,
            str1_start_pointer,
            lambda _counter, a, b: cycle_body(str1_start_pointer, _counter),
            return_counter=True,
            load_counter=False
        )
        Loop.data(
            compiler,
            str2_start_pointer,
            lambda _counter, a, b: cycle_body(str2_start_pointer, _counter, counter),
            load_counter=False
        )

        # Отдаем на стек указатель на начало подстроки для дальнейшего использования
        compiler.code.add(Commands.PUSH, [new_str_start_pointer])

    @staticmethod
    def strmake(compiler):
        """ Генерация инструкций для создания строки заданной длины с повторяющимся символом """
        str_start_pointer = compiler.environment.add_local_var(Types.INT)
        str_length = compiler.environment.add_local_var(Types.INT)
        basis_symbol = compiler.environment.add_local_var(Types.INT)

        finish_label = compiler.labels.create()

        # Сохраняем длину строки в переменную
        compiler.code.add(Commands.POP, str_length)\
            .add(Commands.POP, basis_symbol)

        # Выделяем память = указанной длине строки +1 (плюс маркер конца строки - 0)
        compiler.code.add(Commands.MOV, [Registers.EAX, str_length])\
            .add(Commands.ADD, [Registers.EAX, 1])
        Malloc(compiler).call()
        compiler.code.add(Commands.MOV, [str_start_pointer, Registers.EAX])

        def cycle_body(_counter, b, c):
            compiler.code.add(Commands.MOV, [Registers.EAX, _counter])\
                .add(Commands.MOV, [Registers.EBX, str_length])\
                .add(Commands.CMP, [Registers.EAX, Registers.EBX])

            # Если уже прочитали и записали подстркоу требуемой длины - выходим из цикла
            compiler.code.add(Commands.JZ, finish_label)
            # Загружаем очередной символ подстроки из heap memory
            compiler.code.add(Commands.PUSH, basis_symbol)
            dbstore(compiler, str_start_pointer, _counter)

        counter = Loop.simple(compiler, cycle_body, return_counter=True)

        # Сюда переходим после того, как запишем нужное количество символов в создаваемую строку
        compiler.code.add_label(finish_label)

        # Дописываем 0 в последнюю ячейку памяти - это маркер конца строки
        compiler.code.add(Commands.PUSH, 0)
        dbstore(compiler, str_start_pointer, counter)

        # Отдаем на стек указатель на начало созданной строки для дальнейшего использования
        compiler.code.add(Commands.PUSH, str_start_pointer)

    @staticmethod
    def strcmp(compiler):
        """ Генерация инструкций для посимвольного сравнивания двух строк """
        str1_start_pointer = compiler.environment.add_local_var(Types.INT)
        str2_start_pointer = compiler.environment.add_local_var(Types.INT)

        eq_label = compiler.labels.create()
        not_eq_label = compiler.labels.create()
        larger_label = compiler.labels.create()
        finish_label = compiler.labels.create()

        compiler.code.add(Commands.POP, str1_start_pointer)\
            .add(Commands.POP, str2_start_pointer)

        def cycle_body(_counter, a, continue_label):
            # Загружаем n-ный символ 1-й строки
            dbload(compiler, str1_start_pointer, _counter, size='byte')
            # Дублируем на стек для дальнейшей проверки (чтобы не загружать снова)
            compiler.code.add(Commands.POP, Registers.EAX)\
                .add(Commands.PUSH, Registers.EAX)\
                .add(Commands.PUSH, Registers.EAX)
            # Загружаем n-ный символ 2-й строки
            dbload(compiler, str2_start_pointer, _counter, size='byte')
            compiler.code.add(Commands.POP, Registers.EAX)\
                .add(Commands.POP, Registers.EBX)

            compiler.code.add(Commands.CMP, [Registers.EAX, Registers.EBX])
            # Если символы не равны, сразу переходим в секцию not_eq_label и выясняем уже там - какой из них больше
            # Это также работает, когда мы достиги конца одной из строк (какой-то символ и 0)
            compiler.code.add(Commands.JNZ, not_eq_label)

            # Сравниваем с 0 ранее продублированный символ (1-й строки) - если он равен нулю, то равен и второй,
            # т. к. в эту секцию мы попадаем только при равенстве обоих символов
            compiler.code.add(Commands.POP, Registers.EAX)\
                .add(Commands.CMP, [Registers.EAX, 0])
            # 0 говорит о достижении конца строки - если это не 0, то продолжаем цикл
            compiler.code.add(Commands.JNZ, continue_label)
            # Сюда попадаем, когда достигли конца одновременно двух строк - т. е. они полностью равны
            compiler.code.add(Commands.JMP, eq_label)

        counter = Loop.simple(compiler, cycle_body, return_counter=True)

        # Секция полного равенства строк: пишем на стек 0
        compiler.code.add_label(eq_label)\
            .add(Commands.PUSH, 0)\
            .add(Commands.JMP, finish_label)

        # Секция неравенства строк
        compiler.code.add_label(not_eq_label)
        # Загружаем только второй символ - первый у нас уже содержится на стеке (см. тело цикла)
        dbload(compiler, str2_start_pointer, counter, size='byte')
        # Сравниваем символы оператором <
        compiler.code.add(Commands.POP, Registers.EAX)\
            .add(Commands.POP, Registers.EBX)\
            .add(Commands.CMP, [Registers.EAX, Registers.EBX])

        compiler.code.add(Commands.JG, larger_label)\
            .add(Commands.PUSH, -1)\
            .add(Commands.JMP, finish_label)

        compiler.code.add_label(larger_label)\
            .add(Commands.PUSH, 1)

        compiler.code.add_label(finish_label)
