from ..Helpers.base import *
from ..Helpers.loop import Loop

from ..Utils.malloc import malloc


class StringCompiler:
    pass


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
    malloc(compiler)

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
