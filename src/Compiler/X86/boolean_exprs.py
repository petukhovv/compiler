# -*- coding: utf-8 -*-

from pprint import pprint

from Utils.labels import *

from Helpers.types import *

""" Мапа: арифметический оператор в языке программирования - соответствующая jump-инструкция в ASM """
relop_compare_map = {
    '==':   'je',
    '!=':   'jne',
    '<':    'jg',
    '<=':   'jge',
    '>':    'jl',
    '>=':   'jle'
}

""" Компиляция логического выражения """
def relop_bexp(compiler, op, left, right):
    left.compile_x86(compiler)
    right.compile_x86(compiler)
    compiler.code.add('pop', ['eax'])
    compiler.code.add('pop', ['ebx'])

    compiler.code.add('cmp', ['ebx', 'eax'])

    true_result_label = TrueResult(compiler)

    compiler.code.add('mov', ['eax', 0])
    compiler.code.add(relop_compare_map[op], [true_result_label.get()])
    true_result_label.add_return()
    compiler.code.add('push', ['eax'])

    return Types.INT
