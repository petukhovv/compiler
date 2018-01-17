# -*- coding: utf-8 -*-

from .Helpers.types import *

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
        'operator': 'idiv',
        'operands': ['ebx']
    },
    '%': {
        'operator': 'div',
        'operands': ['ebx']
    }
}


def int_aexp(compiler, i):
    """ Компиляция числа """
    compiler.code.add('mov', ['eax', i])
    compiler.code.add('push', ['eax'])

    return compiler.commands.set_and_return_type(Types.INT)


def binop_aexp(compiler, op, left, right):
    """ Компиляция арифметического выражения """
    left.compile_x86(compiler)
    compiler.commands.clean_type()
    right.compile_x86(compiler)
    compiler.commands.clean_type()
    compiler.code.add('pop', ['ebx'])
    compiler.code.add('pop', ['eax'])

    compiler.code.add(binop_compare_map[op]['operator'], binop_compare_map[op]['operands'])

    if op == '%':
        compiler.code.add('movzx', ['eax', 'dx'])
    elif op == '/':
        compiler.code.add('movzx', ['eax', 'ax'])

    compiler.code.add('push', ['eax'])

    return compiler.commands.set_and_return_type(Types.INT)


def var_aexp(compiler, name, context, value_type):
    """ Компиляция переменной """
    if context == 'assign':
        compiler.bss.vars.add(name, 'resb', 4, value_type)
        compiler.code.add('pop', [compiler.bss.vars.get(name)])
    else:
        compiler.code.add('mov', ['eax', compiler.bss.vars.get(name)])
        compiler.code.add('push', ['eax'])
        compile_time_type = compiler.bss.vars.get_compile_time_type(name)

        return compiler.commands.set_and_return_type(compile_time_type)
