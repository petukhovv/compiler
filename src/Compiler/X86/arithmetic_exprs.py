# -*- coding: utf-8 -*-

""" Компиляция числа """
def int_aexp(compiler, register, i):
    compiler.code.add('mov', [register, i])

""" Компиляция арифметического выражения """
def binop_aexp(compiler, op, left, right):
    left.compile_x86(compiler, 'eax')
    right.compile_x86(compiler, 'ebx')

    compiler.code.add('add', ['eax', 'ebx'])
