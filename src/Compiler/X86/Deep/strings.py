from ..Helpers.base import *
from ..Helpers.loop import Loop

from ..Utils.malloc import Malloc
from ..Helpers.commands import Commands


class StringCompiler:
    @staticmethod
    def store(compiler):
        """ Генерация инструкций для записи строки из стека в heap memory. """
        str_start_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        end_str_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)

        # Добавляем к требуемому размеру памяти 1 - для escape-нуля (маркера конца строки)
        compiler.code.add(Commands.POP, ['eax'])
        compiler.code.add(Commands.ADD, ['eax', 1])
        compiler.code.add(Commands.PUSH, ['eax'])
        compiler.code.add(Commands.PUSH, ['eax'])
        # Выделяем память размером = числу на стеке (ранее мы записали туда длину строки)
        Malloc(compiler).call()
        compiler.code.add(Commands.MOV, ['dword [%s]' % str_start_pointer, 'eax'])

        # Выносим инвариант цикла - указатель на конец строки - в переменную
        compiler.code.add(Commands.POP, ['ebx'])
        compiler.code.add(Commands.ADD, ['eax', 'ebx'])
        compiler.code.add(Commands.MOV, ['dword [%s]' % end_str_pointer, 'eax'])

        def cycle_body(_counter, b, c):
            # Последовательно сохраняем все символы в выделенной памяти в обратном порядке (т. к. берем со стека)
            dbstore(compiler, end_str_pointer, _counter, invert=True, value=-2)

        counter = Loop.stack(compiler, cycle_body, load_counter=False, return_counter=True)

        # Дописываем 0 в последнюю ячейку памяти - это маркер конца строки
        compiler.code.add(Commands.PUSH, [0])
        dbstore(compiler, str_start_pointer, counter)

        # Отдаем на стек указатель на начало строки для дальнейшего использования
        compiler.code.add(Commands.PUSH, ['dword [%s]' % str_start_pointer])

    @staticmethod
    def strlen(compiler):
        """ Генерация инструкций для получения длины строки, находящейся на стеке. """
        str_start_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        # Разыменовываем лежащий на стеке указатель и записываем его в переменную
        compiler.code.add(Commands.POP, ['dword [%s]' % str_start_pointer])

        # Считываем строку из памяти до конца (пока не встретим 0), подсчитывая кол-во символов (его кладем на стек)
        Loop.data(compiler, str_start_pointer)

    @staticmethod
    def strget(compiler, type):
        """ Генерация инструкций для получения определенного символа строки """
        # Прибавляем к номеру ячейки с началом строки номер требуемого символа (offset)
        compiler.code.add(Commands.POP, ['eax'])
        compiler.code.add(Commands.POP, ['ebx'])
        compiler.code.add(Commands.ADD, ['eax', 'ebx'])
        # Загружаем на стек символ по номеру его ячейки в heap memory
        compiler.code.add(Commands.MOVZX, ['ebx', 'byte [eax]'])
        compiler.code.add(Commands.PUSH, ['ebx'])

    @staticmethod
    def strset(compiler, type):
        """ Генерация инструкций для замены определенного символа строки """
        # Вычисляем ячейки heap memory, где находится заменяемый символ
        compiler.code.add(Commands.POP, ['eax'])
        compiler.code.add(Commands.POP, ['ebx'])
        compiler.code.add(Commands.ADD, ['eax', 'ebx'])
        compiler.code.add(Commands.POP, ['ebx'])

        # Производим замену символа
        compiler.code.add(Commands.MOV, ['byte [eax]', 'bl'])

    @staticmethod
    def strsub(compiler, type):
        """ Генерация инструкций для получение подстроки строки """
        substr_length = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        substr_start_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        start_substr_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        end_substr_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)

        finish_label = compiler.labels.create()

        # Сохраняем длину подстроки
        compiler.code.add(Commands.POP, ['dword [%s]' % substr_length])

        compiler.code.add(Commands.POP, ['eax'])
        compiler.code.add(Commands.POP, ['ebx'])
        compiler.code.add(Commands.ADD, ['eax', 'ebx'])
        compiler.code.add(Commands.MOV, ['dword [%s]' % substr_start_pointer, 'eax'])

        # Выделяем память размером = длине подстроки + 1 (для escape нуля)
        compiler.code.add(Commands.MOV, ['eax', 'dword [%s]' % substr_length])
        compiler.code.add(Commands.ADD, ['eax', 1])
        Malloc(compiler).call()
        compiler.code.add(Commands.MOV, ['dword [%s]' % start_substr_pointer, 'eax'])

        compiler.code.add(Commands.MOV, ['eax', 'dword [%s]' % substr_length])
        compiler.code.add(Commands.MOV, ['ebx', 'dword [%s]' % start_substr_pointer])
        compiler.code.add(Commands.ADD, ['eax', 'ebx'])
        compiler.code.add(Commands.MOV, ['dword [%s]' % end_substr_pointer, 'eax'])

        # Кладем на стек 0 - маркер конца строки
        compiler.code.add(Commands.PUSH, [0])
        dbstore(compiler, end_substr_pointer, None)

        def cycle_body(_counter, a, b):
            compiler.code.add(Commands.MOV, ['eax', 'dword [%s]' % _counter])
            compiler.code.add(Commands.MOV, ['ebx', 'dword [%s]' % substr_length])
            compiler.code.add(Commands.CMP, ['eax', 'ebx'])
            # Если уже прочитали и записали подстркоу требуемой длины - выходим из цикла
            compiler.code.add(Commands.JZ, [finish_label])
            # Загружаем очередной символ подстроки из heap memory
            dbload(compiler, substr_start_pointer, _counter)
            dbstore(compiler, start_substr_pointer, _counter)

        Loop.data(compiler, substr_start_pointer, cycle_body, load_counter=False)

        compiler.code.add(str(finish_label) + ':', [])
        # Отдаем на стек указатель на начало подстроки для дальнейшего использования
        compiler.code.add(Commands.PUSH, ['dword [%s]' % start_substr_pointer])

    @staticmethod
    def strdup(compiler, type):
        """ Генерация инструкций для дублирования строки """
        substr_length = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        str_start_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        new_str_start_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        new_end_str_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        # Разыменовываем лежащий на стеке указатель и записываем его в переменную
        compiler.code.add(Commands.POP, ['dword [%s]' % str_start_pointer])

        # Считываем строку из памяти до конца (пока не встретим 0), подсчитывая кол-во символов (его кладем на стек)
        Loop.data(compiler, str_start_pointer)
        compiler.code.add(Commands.POP, ['eax'])
        compiler.code.add(Commands.MOV, ['dword [%s]' % substr_length, 'eax'])
        Malloc(compiler).call()
        compiler.code.add(Commands.MOV, ['dword [%s]' % new_str_start_pointer, 'eax'])

        compiler.code.add(Commands.MOV, ['eax', 'dword [%s]' % substr_length])
        compiler.code.add(Commands.MOV, ['ebx', 'dword [%s]' % new_str_start_pointer])
        compiler.code.add(Commands.ADD, ['eax', 'ebx'])
        compiler.code.add(Commands.MOV, ['dword [%s]' % new_end_str_pointer, 'eax'])

        # Кладем на стек 0 - маркер конца строки
        compiler.code.add(Commands.PUSH, [0])
        dbstore(compiler, new_end_str_pointer, None)

        def cycle_body(_counter, a, b):
            dbload(compiler, str_start_pointer, _counter)
            dbstore(compiler, new_str_start_pointer, _counter)

        # Читаем строку и кладем её на стек
        Loop.data(compiler, str_start_pointer, cycle_body, load_counter=False)

        # Отдаем на стек указатель на начало подстроки для дальнейшего использования
        compiler.code.add(Commands.PUSH, ['dword [%s]' % new_str_start_pointer])

    @staticmethod
    def strcat_calc_length(compiler):
        # compiler.code.add(Commands.PUSH, ['[esp + 4]'])
        compiler.code.add(Commands.POP, ['eax'])
        compiler.code.add(Commands.POP, ['ebx'])
        compiler.code.add(Commands.PUSH, ['eax'])
        compiler.code.add(Commands.PUSH, ['ebx'])
        compiler.code.add(Commands.PUSH, ['eax'])
        compiler.code.add(Commands.PUSH, ['ebx'])

        StringCompiler.strlen(compiler)
        compiler.code.add(Commands.POP, ['eax'])
        compiler.code.add(Commands.POP, ['ebx'])
        compiler.code.add(Commands.PUSH, ['eax'])
        compiler.code.add(Commands.PUSH, ['ebx'])
        StringCompiler.strlen(compiler)
        compiler.code.add(Commands.POP, ['eax'])
        compiler.code.add(Commands.POP, ['ebx'])
        compiler.code.add(Commands.ADD, ['eax', 'ebx'])
        compiler.code.add(Commands.PUSH, ['eax'])

    @staticmethod
    def strcat(compiler):
        """ Генерация инструкций для дублирования первой из конкатенируемых строки """
        str_length = compiler.bss.vars.add(None, 'resb', 4, Types.INT)

        new_str_start_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        new_end_str_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)

        str1_start_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        str2_start_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)

        counter_with_offset = compiler.bss.vars.add(None, 'resb', 4, Types.INT)

        compiler.code.add(Commands.POP, ['eax'])
        compiler.code.add(Commands.ADD, ['eax', 1])
        compiler.code.add(Commands.POP, ['dword [%s]' % str1_start_pointer])
        compiler.code.add(Commands.POP, ['dword [%s]' % str2_start_pointer])
        compiler.code.add(Commands.MOV, ['dword [%s]' % str_length, 'eax'])
        Malloc(compiler).call()

        # Разыменовываем лежащий на стеке указатель и записываем его в переменную
        compiler.code.add(Commands.MOV, ['dword [%s]' % new_str_start_pointer, 'eax'])
        compiler.code.add(Commands.MOV, ['ebx', 'dword [%s]' % str_length])
        compiler.code.add(Commands.ADD, ['eax', 'ebx'])
        compiler.code.add(Commands.MOV, ['dword [%s]' % new_end_str_pointer, 'eax'])

        compiler.code.add(Commands.PUSH, [0])
        dbstore(compiler, new_end_str_pointer, None)

        def cycle_body(str_start_pointer, _counter, offset=None):
            dbload(compiler, str_start_pointer, _counter)
            if offset:
                compiler.code.add(Commands.MOV, ['eax', 'dword [%s]' % _counter])
                compiler.code.add(Commands.MOV, ['ebx', 'dword [%s]' % offset])
                compiler.code.add(Commands.ADD, ['eax', 'ebx'])
                compiler.code.add(Commands.MOV, ['dword [%s]' % counter_with_offset, 'eax'])
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
        compiler.code.add(Commands.PUSH, ['dword [%s]' % new_str_start_pointer])

    @staticmethod
    def strmake(compiler):
        """ Генерация инструкций для создания строки заданной длины с повторяющимся символом """
        str_start_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        str_length = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        basis_symbol = compiler.bss.vars.add(None, 'resb', 4, Types.CHAR)

        finish_label = compiler.labels.create()

        # Сохраняем длину строки в переменную
        compiler.code.add(Commands.POP, ['dword [%s]' % str_length])
        compiler.code.add(Commands.POP, ['dword [%s]' % basis_symbol])

        # Выделяем память = указанной длине строки +1 (плюс маркер конца строки - 0)
        compiler.code.add(Commands.MOV, ['eax', 'dword [%s]' % str_length])
        Malloc(compiler).call()
        compiler.code.add(Commands.MOV, ['dword [%s]' % str_start_pointer, 'eax'])

        def cycle_body(_counter, b, c):
            compiler.code.add(Commands.MOV, ['eax', 'dword [%s]' % _counter])
            compiler.code.add(Commands.MOV, ['ebx', 'dword [%s]' % str_length])
            compiler.code.add(Commands.CMP, ['eax', 'ebx'])

            # Если уже прочитали и записали подстркоу требуемой длины - выходим из цикла
            compiler.code.add(Commands.JZ, [finish_label])
            # Загружаем очередной символ подстроки из heap memory
            compiler.code.add(Commands.PUSH, ['dword [%s]' % basis_symbol])
            dbstore(compiler, str_start_pointer, _counter)

        counter = Loop.simple(compiler, cycle_body, return_counter=True)

        # Сюда переходим после того, как запишем нужное количество символов в создаваемую строку
        compiler.code.add(str(finish_label) + ':', [])

        # Дописываем 0 в последнюю ячейку памяти - это маркер конца строки
        compiler.code.add(Commands.PUSH, [0])
        dbstore(compiler, str_start_pointer, counter)

        # Отдаем на стек указатель на начало созданной строки для дальнейшего использования
        compiler.code.add(Commands.PUSH, ['dword [%s]' % str_start_pointer])

    @staticmethod
    def strcmp(compiler):
        """ Генерация инструкций для посимвольного сравнивания двух строк """
        str1_start_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        str2_start_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)

        eq_label = compiler.labels.create()
        not_eq_label = compiler.labels.create()
        larger_label = compiler.labels.create()
        finish_label = compiler.labels.create()

        compiler.code.add(Commands.POP, ['dword [%s]' % str1_start_pointer])
        compiler.code.add(Commands.POP, ['dword [%s]' % str2_start_pointer])

        def cycle_body(_counter, a, continue_label):
            # Загружаем n-ный символ 1-й строки
            dbload(compiler, str1_start_pointer, _counter, size='byte')
            # Дублируем на стек для дальнейшей проверки (чтобы не загружать снова)
            compiler.code.add(Commands.POP, ['eax'])
            compiler.code.add(Commands.PUSH, ['eax'])
            compiler.code.add(Commands.PUSH, ['eax'])
            # Загружаем n-ный символ 2-й строки
            dbload(compiler, str2_start_pointer, _counter, size='byte')
            compiler.code.add(Commands.POP, ['eax'])
            compiler.code.add(Commands.POP, ['ebx'])

            compiler.code.add(Commands.CMP, ['eax', 'ebx'])
            # Если символы не равны, сразу переходим в секцию not_eq_label и выясняем уже там - какой из них больше
            # Это также работает, когда мы достиги конца одной из строк (какой-то символ и 0)
            compiler.code.add(Commands.JNZ, [not_eq_label])

            # Сравниваем с 0 ранее продублированный символ (1-й строки) - если он равен нулю, то равен и второй,
            # т. к. в эту секцию мы попадаем только при равенстве обоих символов
            compiler.code.add(Commands.POP, ['eax'])
            compiler.code.add(Commands.CMP, ['eax', 0])
            # 0 говорит о достижении конца строки - если это не 0, то продолжаем цикл
            compiler.code.add(Commands.JNZ, [continue_label])
            # Сюда попадаем, когда достигли конца одновременно двух строк - т. е. они полностью равны
            compiler.code.add(Commands.JMP, [eq_label])

        counter = Loop.simple(compiler, cycle_body, return_counter=True)

        # Секция полного равенства строк: пишем на стек 0
        compiler.code.add(str(eq_label) + ':', [])
        compiler.code.add(Commands.PUSH, [0])
        compiler.code.add(Commands.JMP, [finish_label])

        # Секция неравенства строк
        compiler.code.add(str(not_eq_label) + ':', [])
        # Загружаем только второй символ - первый у нас уже содержится на стеке (см. тело цикла)
        dbload(compiler, str2_start_pointer, counter, size='byte')
        # Сравниваем символы оператором <
        compiler.code.add(Commands.POP, ['eax'])
        compiler.code.add(Commands.POP, ['ebx'])
        compiler.code.add(Commands.CMP, ['eax', 'ebx'])

        compiler.code.add(Commands.JG, [larger_label])
        compiler.code.add(Commands.PUSH, [-1])
        compiler.code.add(Commands.JMP, [finish_label])

        compiler.code.add(str(larger_label) + ':', [])
        compiler.code.add(Commands.PUSH, [1])

        compiler.code.add(str(finish_label) + ':', [])
