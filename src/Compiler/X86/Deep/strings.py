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
        compiler.code.add('pop', ['eax'])
        compiler.code.add('mov', ['dword [%s]' % str_start_pointer, 'eax'])

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
