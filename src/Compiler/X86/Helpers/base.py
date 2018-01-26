# -*- coding: utf-8 -*-

from .commands import *
from .types import *


def dbload(compiler, address, offset, size='dword'):
    """ Хелпер для генерации инструкций для загрузки значения из heap memory по заданному адресу с заданным смещением """
    compiler.code.add(Commands.MOV, ['eax', 'dword [%s]' % address])
    compiler.code.add(Commands.MOV, ['ebx', 'dword [%s]' % offset])
    compiler.code.add(Commands.ADD, ['eax', 'ebx'])

    if size == 'byte':
        compiler.code.add(Commands.MOVZX, ['eax', 'byte [eax]'])
    else:
        compiler.code.add(Commands.MOV, ['eax', 'dword [eax]'])

    compiler.code.add(Commands.PUSH, ['eax'])


def dbstore(compiler, address, offset, invert=False, value=0):
    """ Хелпер для генерации инструкций для сохранения значения в heap memory по заданному адресу с заданным смещением """
    compiler.code.add(Commands.MOV, ['eax', 'dword [%s]' % address])

    if offset is None:
        compiler.code.add(Commands.MOV, ['ebx', 0])
    else:
        compiler.code.add(Commands.MOV, ['ebx', 'dword [%s]' % offset])
    compiler.code.add(Commands.SUB if invert else Commands.ADD, ['eax', 'ebx'])

    compiler.code.add(Commands.ADD, ['eax', value])
    compiler.code.add(Commands.POP, ['ebx'])
    compiler.code.add(Commands.MOV, ['byte [eax]', 'bl'])


def calc_arr_element_address(compiler, arr_pointer, counter):
    """ Хелпер для генерации инструкций для сохранения значения в heap memory по заданному адресу с заданным смещением """
    element_place = compiler.bss.vars.add(None, 'resb', 4, Types.INT)
    compiler.code.add(Commands.MOV, ['eax', 'dword [%s]' % counter])
    compiler.code.add(Commands.MOV, ['ebx', 2 * 4])
    compiler.code.add(Commands.MUL, ['ebx'])
    compiler.code.add(Commands.MOV, ['ebx', 'dword [%s]' % arr_pointer])
    compiler.code.add(Commands.ADD, ['eax', 'ebx'])

    compiler.code.add(Commands.MOV, ['dword [%s]' % element_place, 'eax'])

    return element_place
