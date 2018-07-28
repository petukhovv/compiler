# -*- coding: utf-8 -*-

from .Deep.strings import *


def char(compiler, character):
    """ Компиляция выражения "символ" """
    compiler.code.add(Commands.PUSH, ord(character))

    return compiler.types.set(Types.CHAR)


def string(compiler, characters):
    """ Компиляция выражения "строка" """
    str_length = len(characters)
    str_pointer = compiler.environment.add_local_var(size=str_length + 5)

    compiler.code.add(Commands.MOV, [Registers.EAX, str_pointer['pointer']])\
        .add(Commands.ADD, [Registers.EAX, -str_pointer['offset'] - str_length - 4])\
        .add(Commands.MOV, ['dword [%s-%d]' % (str_pointer['pointer'], str_pointer['offset']), Registers.EAX])\
        .add(Commands.MOV, ['byte [%s-%d]' % (str_pointer['pointer'], str_pointer['offset'] + 4), 0])

    for i, character in enumerate(reversed(characters)):
        compiler.code.add(Commands.MOV,
                          ['byte [%s-%d]' % (str_pointer['pointer'], i + 5 + str_pointer['offset']), ord(character)])

    compiler.code.add(Commands.MOV, [Registers.EAX, 'dword [%s-%d]' % (str_pointer['pointer'], str_pointer['offset'])])\
        .add(Commands.PUSH, Registers.EAX)

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
    args.elements[0].compile_asm(compiler)
    compiler.types.pop()
    StringCompiler.strget(compiler)

    return compiler.types.set(Types.CHAR)


def strset(compiler, args):
    """ Компиляция built-in функции strset (задание символа строки) """
    args.elements[2].compile_asm(compiler)
    compiler.types.pop()
    args.elements[1].compile_asm(compiler)
    compiler.types.pop()
    args.elements[0].compile_asm(compiler)
    compiler.types.pop()
    StringCompiler.strset(compiler)


def strsub(compiler, args):
    """ Компиляция built-in функции strsub (взятие подстроки строки) """
    args.elements[1].compile_asm(compiler)
    compiler.types.pop()
    args.elements[0].compile_asm(compiler)
    compiler.types.pop()
    args.elements[2].compile_asm(compiler)
    compiler.types.pop()
    StringCompiler.strsub(compiler)

    return compiler.types.set(Types.STRING)


def strdup(compiler, args):
    """ Компиляция built-in функции strdup (дублирование строки) """
    args.elements[0].compile_asm(compiler)
    compiler.types.pop()
    StringCompiler.strdup(compiler)

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
