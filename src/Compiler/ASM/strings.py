# -*- coding: utf-8 -*-

from .Deep.strings import *


def char(compiler, character, need_typify=True, address=None):
    """ Компиляция выражения "символ" """
    if address:
        compiler.code.add(Commands.MOV, ['byte [%s]' % address, ord(character)])
    else:
        compiler.code.add(Commands.PUSH, [ord(character)])
    if need_typify:
        return compiler.types.set(Types.CHAR)


def string(compiler, characters):
    """ Компиляция выражения "строка" """
    str_length = len(characters)
    str_pointer = compiler.vars.add(None, 'resb', str_length + 2, Types.INT)

    for i, character in enumerate(characters):
        char(compiler, character, need_typify=False, address="%s+%d" % (str_pointer, i))

    compiler.code.add(Commands.MOV, ['byte [%s+%d]' % (str_pointer, str_length), 0])
    compiler.code.add(Commands.PUSH, [str_pointer])

    return compiler.types.set(Types.STRING)


def strlen(compiler, args):
    """ Компиляция built-in функции strlen (длина строки) """
    args.elements[0].compile_asm(compiler)
    compiler.types.pop()

    StringCompiler.strlen(compiler)

    return compiler.types.set(Types.INT)


def strget(compiler, args):
    """ Компиляция built-in функции strget (получение символа строки) """
    # Порядок компиляции аргументов здесь и ниже задаём удобным для дальнейшей работы образом
    args.elements[1].compile_asm(compiler)
    compiler.types.pop()
    array_type = args.elements[0].compile_asm(compiler)
    compiler.types.pop()
    StringCompiler.strget(compiler, array_type)

    return compiler.types.set(Types.CHAR)


def strset(compiler, args):
    """ Компиляция built-in функции strset (задание символа строки) """
    args.elements[2].compile_asm(compiler)
    compiler.types.pop()
    args.elements[1].compile_asm(compiler)
    compiler.types.pop()
    array_type = args.elements[0].compile_asm(compiler)
    compiler.types.pop()
    StringCompiler.strset(compiler, array_type)


def strsub(compiler, args):
    """ Компиляция built-in функции strsub (взятие подстроки строки) """
    args.elements[1].compile_asm(compiler)
    compiler.types.pop()
    array_type = args.elements[0].compile_asm(compiler)
    compiler.types.pop()
    args.elements[2].compile_asm(compiler)
    compiler.types.pop()
    StringCompiler.strsub(compiler, array_type)

    return compiler.types.set(Types.STRING)


def strdup(compiler, args):
    """ Компиляция built-in функции strdup (дублирование строки) """
    array_type = args.elements[0].compile_asm(compiler)
    compiler.types.pop()
    StringCompiler.strdup(compiler, array_type)

    return compiler.types.set(Types.STRING)


def strcat(compiler, args):
    """ Компиляция built-in функции strcat (конкатенация двух строк) """
    args.elements[0].compile_asm(compiler)
    compiler.types.pop()
    args.elements[1].compile_asm(compiler)
    compiler.types.pop()

    StringCompiler.strcat_calc_length(compiler)
    StringCompiler.strcat(compiler)

    return compiler.types.set(Types.STRING)


def strmake(compiler, args):
    """ Компиляция built-in функции strmake (создание строки из n одинаковых символов) """
    args.elements[1].compile_asm(compiler)
    compiler.types.pop()
    args.elements[0].compile_asm(compiler)
    compiler.types.pop()
    StringCompiler.strmake(compiler)

    return compiler.types.set(Types.STRING)


def strcmp(compiler, args):
    """ Компиляция built-in функции strcmp (посимвольное сравнение двух строк) """
    args.elements[0].compile_asm(compiler)
    compiler.types.pop()
    args.elements[1].compile_asm(compiler)
    compiler.types.pop()
    StringCompiler.strcmp(compiler)

    return compiler.types.set(Types.INT)
