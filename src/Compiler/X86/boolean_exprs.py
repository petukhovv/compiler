# -*- coding: utf-8 -*-

from .Helpers.types import *
from .Utils.labels import *

""" Мапа: арифметический оператор в языке программирования - соответствующая jump-инструкция в ASM """
relop_compare_map = {
    '==':   'je',
    '!=':   'jne',
    '<':    'jg',
    '<=':   'jge',
    '>':    'jl',
    '>=':   'jle'
}


def relop_bexp(compiler, op, left, right):
    """ Компиляция логического выражения """
    left.compile_x86(compiler)
    compiler.commands.clean_type()
    right.compile_x86(compiler)
    compiler.commands.clean_type()
    compiler.code.add('pop', ['ebx'])
    compiler.code.add('pop', ['eax'])

    compiler.code.add('cmp', ['ebx', 'eax'])

    true_result_label = TrueResult(compiler)

    compiler.code.add('mov', ['eax', 0])
    compiler.code.add(relop_compare_map[op], [true_result_label.get()])
    true_result_label.add_return()
    compiler.code.add('push', ['eax'])

    return compiler.commands.set_and_return_type(Types.INT)


def and_bexp(compiler, left, right):
    """ Компиляция оператора логического "И" (and) """
    finish_label = compiler.labels.create()
    finish_false_label = compiler.labels.create()

    left.compile_x86(compiler)
    compiler.commands.clean_type()
    compiler.code.add('pop', ['eax'])

    # Если первый операнд == 0, второй уже не проверяем,
    # а сразу переходим к метке ложного результата (ленивая проверка)
    compiler.code.add('cmp', ['eax', 1])
    compiler.code.add('jnz near', [finish_false_label])

    # Иначе будем проверять и второй
    right.compile_x86(compiler)
    compiler.commands.clean_type()
    compiler.code.add('pop', ['eax'])

    # Если второй операнд == 0, то переходим к метке ложного результата
    compiler.code.add('cmp', ['eax', 1])
    compiler.code.add('jnz near', [finish_false_label])

    # Если оба операнда == 1, то в целом результат выполнения and - 1 - его и пишем в стек
    # и переходим к метке полного завершения выполнения and (минуя секцию ложного результата).
    compiler.code.add('mov', ['eax', 1])
    compiler.code.add('jmp near', [finish_label])

    # Секция ложного результата, пишем в стек 0
    compiler.code.add(finish_false_label + ':', [])
    compiler.code.add('mov', ['eax', 0])

    # Полное завершения выполнения and
    compiler.code.add(finish_label + ':', [])

    compiler.code.add('push', ['eax'])

    return compiler.commands.set_and_return_type(Types.BOOL)
