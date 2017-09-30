# -*- coding: utf-8 -*-

from pprint import pprint

""" Мапа: арифметический оператор в языке программирования - арифметический оператор в ASM-коде """
binop_compare_map = {
    '+': {
        'operator': 'add',
        'operands': ['eax', 'ebx']
    },
    '-': {
        'operator': 'sub',
        'operands': ['eax', 'ebx']
    },
    '*': {
        'operator': 'mul',
        'operands': ['ebx']
    },
    '/': {
        'operator': 'div',
        'operands': ['ebx']
    }
}

""" Компиляция числа """
def int_aexp(compiler, i):
    compiler.code.add('mov', ['eax', i])
    compiler.code.add('push', ['eax'])

""" Компиляция арифметического выражения """
def binop_aexp(compiler, op, left, right):
    left.compile_x86(compiler)
    right.compile_x86(compiler)
    compiler.code.add('pop', ['ebx'])
    compiler.code.add('pop', ['eax'])

    compiler.code.add(binop_compare_map[op]['operator'], binop_compare_map[op]['operands'])
    compiler.code.add('push', ['eax'])
