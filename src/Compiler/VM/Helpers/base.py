# -*- coding: utf-8 -*-

from src.VM.commands import *

class types:
    NONE = 0
    INT = 1
    CHAR = 2
    BOOL = 3
    STRING = 4
    BOXED_ARR = 5
    UNBOXED_ARR = 6
    DYNAMIC = 7

""" Хелпер для компиляции заданных аргументов built-in функций """
def args_compile(args, numbers, commands, data):
    if isinstance(numbers, list):
        for number in numbers:
            args.elements[number].compile_vm(commands, data)
    else:
        args.elements[numbers].compile_vm(commands, data)

""" Хелпер для генерации инструкций для загрузки значения из heap memory по заданному адресу с заданным смещением """
def dbload(address, offset, commands):
    commands.add(Load, address)\
        .add(Load, offset)\
        .add(Add)\
        .add(DBLoad, 0)

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

""" Хелпер для генерации инструкций для загрузки значения из heap memory с адресом = значению на стеке и сохранения его в переменную """
def bload_and_store(variable, commands):
    commands.add(Store, variable)
