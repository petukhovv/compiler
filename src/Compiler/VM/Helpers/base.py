# -*- coding: utf-8 -*-

from commands import *

""" Хелпер для генерации инструкций для загрузки значения из heap memory по заданному адресу с заданным смещением """
def dbload(address, offset, commands):
    commands.add(Load, address)\
        .add(Load, offset)\
        .add(Add)\
        .add(DBLoad, 0)

""" Хелпер для генерации инструкций для загрузки значения из heap memory по заданному адресу с заданным смещением """
def bload(address, offset, commands):
    commands.add(Load, address)\
        .add(Load, offset)\
        .add(Add)\
        .add(BLoad, 0)

""" Хелпер для генерации инструкций для сохранения значения в heap memory по заданному адресу с заданным смещением """
def dbstore(address, offset, commands, invert=False, value=0):
    commands.add(Load, address)
    if offset is None:
        commands.add(Push, 0)
    else:
        commands.add(Load, offset)
    if invert:
        commands.add(Sub)
    else:
        commands.add(Add)
    commands.add(DBStore, value)

""" Хелпер для генерации инструкций для сохранения значения в heap memory по заданному адресу с заданным смещением """
def calc_arr_element_address(commands, data, arr_pointer, counter):
    element_place = data.var()
    commands.add(Load, arr_pointer)
    commands.add(Load, counter)
    commands.add(Push, 2)
    commands.add(Mul)
    commands.add(Add)
    commands.add(Dup)
    commands.add(Store, element_place)

    return element_place
