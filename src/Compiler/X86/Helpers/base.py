# -*- coding: utf-8 -*-

from .commands import *
from .types import *


def dbload(compiler, address, offset, size='dword'):
    """ Хелпер для генерации инструкций для загрузки значения из heap memory по заданному адресу с заданным смещением """
    compiler.code.add('mov', ['eax', 'dword [%s]' % address])
    compiler.code.add('mov', ['ebx', 'dword [%s]' % offset])
    compiler.code.add('add', ['eax', 'ebx'])

    if size == 'byte':
        compiler.code.add('movzx', ['eax', 'byte [eax]'])
    else:
        compiler.code.add('mov', ['eax', 'dword [eax]'])

    compiler.code.add('push', ['eax'])


def dbstore(compiler, address, offset, invert=False, value=0):
    """ Хелпер для генерации инструкций для сохранения значения в heap memory по заданному адресу с заданным смещением """
    compiler.code.add('mov', ['eax', 'dword [%s]' % address])

    if offset is None:
        compiler.code.add('mov', ['ebx', 0])
    else:
        compiler.code.add('mov', ['ebx', 'dword [%s]' % offset])
    compiler.code.add('sub' if invert else 'add', ['eax', 'ebx'])

    compiler.code.add('add', ['eax', value])
    compiler.code.add('pop', ['ebx'])
    compiler.code.add('mov', ['byte [eax]', 'bl'])


def calc_arr_element_address(compiler, arr_pointer, counter):
    """ Хелпер для генерации инструкций для сохранения значения в heap memory по заданному адресу с заданным смещением """
    element_place = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
    compiler.code.add('mov', ['eax', 'dword [%s]' % counter])
    compiler.code.add('mov', ['ebx', 2 * 4])
    compiler.code.add('mul', ['ebx'])
    compiler.code.add('mov', ['ebx', 'dword [%s]' % arr_pointer])
    compiler.code.add('add', ['eax', 'ebx'])

    compiler.code.add('mov', ['dword [%s]' % element_place, 'eax'])

    return element_place
