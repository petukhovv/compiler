# -*- coding: utf-8 -*-

from pprint import pprint

""" Компиляция числа """
def int_aexp(compiler, i):
    compiler.code.add('mov', [compiler.target_register, i])

""" Компиляция арифметического выражения """
def binop_aexp(compiler, op, left, right):
    compiler.target_register = 'eax'
    left.compile_x86(compiler)
    compiler.target_register = 'ebx'
    right.compile_x86(compiler)

    compiler.code.add('add', ['eax', 'ebx'])
