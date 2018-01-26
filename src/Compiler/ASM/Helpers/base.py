# -*- coding: utf-8 -*-

from ..Core.registers import Registers
from ..Core.types import *


def dbload(compiler, address, offset, size='dword'):
    """ Хелпер для генерации инструкций для загрузки значения из heap memory по заданному адресу с заданным смещением """
    compiler.code.add(Commands.MOV, [Registers.EAX, 'dword [%s]' % address])\
        .add(Commands.MOV, [Registers.EBX, 'dword [%s]' % offset])\
        .add(Commands.ADD, [Registers.EAX, Registers.EBX])

    if size == 'byte':
        compiler.code.add(Commands.MOVZX, [Registers.EAX, 'byte [%s]' % Registers.EAX])
    else:
        compiler.code.add(Commands.MOV, [Registers.EAX, 'dword [%s]' % Registers.EAX])

    compiler.code.add(Commands.PUSH, Registers.EAX)


def dbstore(compiler, address, offset, invert=False, value=0):
    """ Хелпер для генерации инструкций для сохранения значения в heap memory по заданному адресу с заданным смещением """
    compiler.code.add(Commands.MOV, [Registers.EAX, 'dword [%s]' % address])

    if offset is None:
        compiler.code.add(Commands.MOV, [Registers.EBX, 0])
    else:
        compiler.code.add(Commands.MOV, [Registers.EBX, 'dword [%s]' % offset])
    compiler.code.add(Commands.SUB if invert else Commands.ADD, [Registers.EAX, Registers.EBX])

    compiler.code.add(Commands.ADD, [Registers.EAX, value])\
        .add(Commands.POP, Registers.EBX)\
        .add(Commands.MOV, ['byte [%s]' % Registers.EAX, Registers.BL])


def calc_arr_element_address(compiler, arr_pointer, counter):
    """ Хелпер для генерации инструкций для сохранения значения в heap memory по заданному адресу с заданным смещением """
    element_place = compiler.vars.add(None, 'resb', 4, Types.INT)

    compiler.code.add(Commands.MOV, [Registers.EAX, 'dword [%s]' % counter])\
        .add(Commands.MOV, [Registers.EBX, 2 * 4])\
        .add(Commands.MUL, Registers.EBX)\
        .add(Commands.MOV, [Registers.EBX, 'dword [%s]' % arr_pointer])\
        .add(Commands.ADD, [Registers.EAX, Registers.EBX])

    compiler.code.add(Commands.MOV, ['dword [%s]' % element_place, Registers.EAX])

    return element_place
