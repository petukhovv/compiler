# -*- coding: utf-8 -*-

from .commands import *
from .types import *


def dbload(compiler, address, offset):
    """ Хелпер для генерации инструкций для загрузки значения из heap memory по заданному адресу с заданным смещением """
    compiler.code.add('mov', ['eax', 'dword [%s]' % address])
    compiler.code.add('mov', ['ebx', 'dword [%s]' % offset])
    compiler.code.add('add', ['eax', 'ebx'])

    compiler.code.add('push', ['dword [eax]'])


def dbstore(compiler, address, offset, invert=False, value=0):
    """ Хелпер для генерации инструкций для сохранения значения в heap memory по заданному адресу с заданным смещением """
    compiler.code.add('mov', ['eax', 'dword [%s]' % address])

    if offset is None:
        compiler.code.add('mov', ['ebx', 0])
    else:
        compiler.code.add('mov', ['ebx', 'dword [%s]' % offset])
    compiler.code.add('add' if invert else 'sub', ['eax', 'ebx'])

    compiler.code.add('add', ['eax', value])
    compiler.code.add('pop', ['dword [eax]'])


def calc_arr_element_address(compiler, arr_pointer, counter):
    """ Хелпер для генерации инструкций для сохранения значения в heap memory по заданному адресу с заданным смещением """
    element_place = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
    compiler.code.add('eax', ['dword [%s]' % counter])
    compiler.code.add('mul', ['eax', 2])
    compiler.code.add('ebx', ['dword [%s]' % arr_pointer])
    compiler.code.add('add', ['eax', 'ebx'])

    compiler.code.add('mov', ['dword [%s]' % element_place, 'eax'])
    compiler.code.add('push', ['eax'])

    return element_place
