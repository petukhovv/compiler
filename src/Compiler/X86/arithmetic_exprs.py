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
    compiler.code.add('mov', [compiler.target_register, i])

""" Компиляция арифметического выражения """
def binop_aexp(compiler, op, left, right):
    compiler.target_register = 'eax'
    left.compile_x86(compiler)
    compiler.target_register = 'ebx'
    right.compile_x86(compiler)

    compiler.code.add(binop_compare_map[op]['operator'], binop_compare_map[op]['operands'])
