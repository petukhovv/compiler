# -*- coding: utf-8 -*-

from .Deep.strings import *


def char(compiler, character, need_typify=True):
    """ Компиляция выражения "символ" """
    compiler.code.add('push', [ord(character)])
    if need_typify:
        return compiler.commands.set_and_return_type(Types.CHAR)


def string(compiler, characters):
    """ Компиляция выражения "строка" """
    compiler.code.add('push', [0])
    for character in characters:
        char(compiler, character, need_typify=False)

    compiler.code.add('push', [len(characters)])
    store(compiler)

    return compiler.commands.set_and_return_type(Types.STRING)
