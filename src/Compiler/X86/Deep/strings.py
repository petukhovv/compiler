from ..Helpers.base import *
from ..Helpers.loop import Loop

from ..Utils.malloc import Malloc


class StringCompiler:
    @staticmethod
    def store(compiler):
        """ Генерация инструкций для записи строки из стека в heap memory. """
        str_start_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        end_str_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)

        # Добавляем к требуемому размеру памяти 1 - для escape-нуля (маркера конца строки)
        compiler.code.add('pop', ['eax'])
        compiler.code.add('add', ['eax', 1])
        compiler.code.add('push', ['eax'])
        compiler.code.add('push', ['eax'])
        # Выделяем память размером = числу на стеке (ранее мы записали туда длину строки)
        Malloc(compiler).call()
        compiler.code.add('mov', ['dword [%s]' % str_start_pointer, 'eax'])

        # Выносим инвариант цикла - указатель на конец строки - в переменную
        compiler.code.add('pop', ['ebx'])
        compiler.code.add('add', ['eax', 'ebx'])
        compiler.code.add('mov', ['dword [%s]' % end_str_pointer, 'eax'])

        def cycle_body(_counter, b, c):
            # Последовательно сохраняем все символы в выделенной памяти в обратном порядке (т. к. берем со стека)
            dbstore(compiler, end_str_pointer, _counter, invert=True, value=-2)

        counter = Loop.stack(compiler, cycle_body, load_counter=False, return_counter=True)

        # Дописываем 0 в последнюю ячейку памяти - это маркер конца строки
        compiler.code.add('push', [0])
        dbstore(compiler, str_start_pointer, counter)

        # Отдаем на стек указатель на начало строки для дальнейшего использования
        compiler.code.add('push', ['dword [%s]' % str_start_pointer])

    @staticmethod
    def strlen(compiler, type):
        """ Генерация инструкций для получения длины строки, находящейся на стеке. """
        str_start_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        # Разыменовываем лежащий на стеке указатель и записываем его в переменную
        compiler.code.add('pop', ['dword [%s]' % str_start_pointer])

        # Считываем строку из памяти до конца (пока не встретим 0), подсчитывая кол-во символов (его кладем на стек)
        Loop.data(compiler, str_start_pointer)

    @staticmethod
    def strget(compiler, type):
        """ Генерация инструкций для получения определенного символа строки """
        # Прибавляем к номеру ячейки с началом строки номер требуемого символа (offset)
        compiler.code.add('pop', ['eax'])
        compiler.code.add('pop', ['ebx'])
        compiler.code.add('add', ['eax', 'ebx'])
        # Загружаем на стек символ по номеру его ячейки в heap memory
        compiler.code.add('movzx', ['ebx', 'byte [eax]'])
        compiler.code.add('push', ['ebx'])

    @staticmethod
    def strset(compiler, type):
        """ Генерация инструкций для замены определенного символа строки """
        # Вычисляем ячейки heap memory, где находится заменяемый символ
        compiler.code.add('pop', ['eax'])
        compiler.code.add('pop', ['ebx'])
        compiler.code.add('add', ['eax', 'ebx'])
        compiler.code.add('pop', ['ebx'])

        # Производим замену символа
        compiler.code.add('mov', ['byte [eax]', 'bl'])

    @staticmethod
    def strsub(compiler, type):
        """ Генерация инструкций для получение подстроки строки """
        substr_length = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        substr_start_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        start_substr_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        end_substr_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)

        finish_label = compiler.labels.create()

        # Сохраняем длину подстроки
        compiler.code.add('pop', ['dword [%s]' % substr_length])

        compiler.code.add('pop', ['eax'])
        compiler.code.add('pop', ['ebx'])
        compiler.code.add('add', ['eax', 'ebx'])
        compiler.code.add('mov', ['dword [%s]' % substr_start_pointer, 'eax'])

        # Выделяем память размером = длине подстроки + 1 (для escape нуля)
        compiler.code.add('mov', ['eax', 'dword [%s]' % substr_length])
        compiler.code.add('add', ['eax', 1])
        Malloc(compiler).call()
        compiler.code.add('mov', ['dword [%s]' % start_substr_pointer, 'eax'])

        compiler.code.add('mov', ['eax', 'dword [%s]' % substr_length])
        compiler.code.add('mov', ['ebx', 'dword [%s]' % start_substr_pointer])
        compiler.code.add('add', ['eax', 'ebx'])
        compiler.code.add('mov', ['dword [%s]' % end_substr_pointer, 'eax'])

        # Кладем на стек 0 - маркер конца строки
        compiler.code.add('push', [0])
        dbstore(compiler, end_substr_pointer, None)

        def cycle_body(_counter, a, b):
            compiler.code.add('mov', ['eax', 'dword [%s]' % _counter])
            compiler.code.add('mov', ['ebx', 'dword [%s]' % substr_length])
            compiler.code.add('cmp', ['eax', 'ebx'])
            # Если уже прочитали и записали подстркоу требуемой длины - выходим из цикла
            compiler.code.add('jz near', [finish_label])
            # Загружаем очередной символ подстроки из heap memory
            dbload(compiler, substr_start_pointer, _counter)
            dbstore(compiler, start_substr_pointer, _counter)

        Loop.data(compiler, substr_start_pointer, cycle_body, load_counter=False)

        compiler.code.add(str(finish_label) + ':', [])
        # Отдаем на стек указатель на начало подстроки для дальнейшего использования
        compiler.code.add('push', ['dword [%s]' % start_substr_pointer])

    @staticmethod
    def strdup(compiler, type):
        """ Генерация инструкций для дублирования строки """
        substr_length = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        str_start_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        new_str_start_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        new_end_str_pointer = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
        # Разыменовываем лежащий на стеке указатель и записываем его в переменную
        compiler.code.add('pop', ['dword [%s]' % str_start_pointer])

        # Считываем строку из памяти до конца (пока не встретим 0), подсчитывая кол-во символов (его кладем на стек)
        Loop.data(compiler, str_start_pointer)
        compiler.code.add('pop', ['eax'])
        compiler.code.add('mov', ['dword [%s]' % substr_length, 'eax'])
        Malloc(compiler).call()
        compiler.code.add('mov', ['dword [%s]' % new_str_start_pointer, 'eax'])

        compiler.code.add('mov', ['eax', 'dword [%s]' % substr_length])
        compiler.code.add('mov', ['ebx', 'dword [%s]' % new_str_start_pointer])
        compiler.code.add('add', ['eax', 'ebx'])
        compiler.code.add('mov', ['dword [%s]' % new_end_str_pointer, 'eax'])

        # Кладем на стек 0 - маркер конца строки
        compiler.code.add('push', [0])
        dbstore(compiler, new_end_str_pointer, None)

        def cycle_body(_counter, a, b):
            dbload(compiler, str_start_pointer, _counter)
            dbstore(compiler, new_str_start_pointer, _counter)

        # Читаем строку и кладем её на стек
        Loop.data(compiler, str_start_pointer, cycle_body)

        # Отдаем на стек указатель на начало подстроки для дальнейшего использования
        compiler.code.add('push', ['dword [%s]' % new_str_start_pointer])
