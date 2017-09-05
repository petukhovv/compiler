# -*- coding: utf-8 -*-

from src.VM.commands import *

""" Хелпер для компиляции заданных аргументов built-in функций """
def args_compile(args, numbers, commands, env):
    if isinstance(numbers, list):
        for number in numbers:
            args.elements[number].compile_vm(commands, env)
    else:
        args.elements[numbers].compile_vm(commands, env)

""" Хелпер для генерации инструкций для загрузки значения из heap memory по заданному адресу с заданным смещением """
def dbload(address, offset, commands):
    commands.add(Load, address)\
        .add(Load, offset)\
        .add(Add)\
        .add(DBLoad, 0)

""" Хелпер для генерации инструкций для сохранения значения в heap memory по заданному адресу с заданным смещением """
def dbstore(address, offset, commands, invert=False, value=0):
    commands.add(Load, address)\
        .add(Load, offset)
    if invert:
        commands.add(Sub)
    else:
        commands.add(Add)
    commands.add(DBStore, value)

""" Хелпер для генерации инструкций для загрузки значения из heap memory с адресом = значению на стеке и сохранения его в переменную """
def bload_and_store(variable, commands):
    commands.add(BLoad, 0)\
        .add(Store, variable)
