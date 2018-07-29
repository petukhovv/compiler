# -*- coding: utf-8 -*-

from ...Deep.strings import StringCompiler
from ...Core.commands import Commands
from ...Core.registers import Registers
from ...Core.types import Types


def char(compiler, node):
    """ Компиляция выражения "символ" """
    compiler.code.add(Commands.PUSH, ord(node.character))

    return compiler.types.set(Types.CHAR)


def string(compiler, node):
    """ Компиляция выражения "строка" """
    str_length = len(node.characters)
    str_pointer = compiler.environment.add_local_var(size=str_length + 5)

    compiler.code.add(Commands.MOV, [Registers.EAX, str_pointer['pointer']])\
        .add(Commands.ADD, [Registers.EAX, -str_pointer['offset'] - str_length - 4])\
        .add(Commands.MOV, ['dword [%s-%d]' % (str_pointer['pointer'], str_pointer['offset']), Registers.EAX])\
        .add(Commands.MOV, ['byte [%s-%d]' % (str_pointer['pointer'], str_pointer['offset'] + 4), 0])

    for i, character in enumerate(reversed(node.characters)):
        compiler.code.add(Commands.MOV,
                          ['byte [%s-%d]' % (str_pointer['pointer'], i + 5 + str_pointer['offset']), ord(character)])

    compiler.code.add(Commands.MOV, [Registers.EAX, 'dword [%s-%d]' % (str_pointer['pointer'], str_pointer['offset'])])\
        .add(Commands.PUSH, Registers.EAX)

    return compiler.types.set(Types.STRING)


def strlen(compiler, node):
    """ Компиляция built-in функции strlen (длина строки) """
    node.args.elements[0].compile_asm(compiler)
    compiler.types.pop()

    StringCompiler.strlen(compiler)

    return compiler.types.set(Types.INT)


def strget(compiler, node):
    """ Компиляция built-in функции strget (получение символа строки) """
    # Порядок компиляции аргументов здесь и ниже задаём удобным для дальнейшей работы образом
    node.args.elements[1].compile_asm(compiler)
    compiler.types.pop()
    node.args.elements[0].compile_asm(compiler)
    compiler.types.pop()
    StringCompiler.strget(compiler)

    return compiler.types.set(Types.CHAR)


def strsub(compiler, node):
    """ Компиляция built-in функции strsub (взятие подстроки строки) """
    node.args.elements[1].compile_asm(compiler)
    compiler.types.pop()
    node.args.elements[0].compile_asm(compiler)
    compiler.types.pop()
    node.args.elements[2].compile_asm(compiler)
    compiler.types.pop()
    StringCompiler.strsub(compiler)

    return compiler.types.set(Types.STRING)


def strdup(compiler, node):
    """ Компиляция built-in функции strdup (дублирование строки) """
    node.args.elements[0].compile_asm(compiler)
    compiler.types.pop()
    StringCompiler.strdup(compiler)

    return compiler.types.set(Types.STRING)


def strcat(compiler, node):
    """ Компиляция built-in функции strcat (конкатенация двух строк) """
    node.args.elements[0].compile_asm(compiler)
    compiler.types.pop()
    node.args.elements[1].compile_asm(compiler)
    compiler.types.pop()

    StringCompiler.strcat_calc_length(compiler)
    StringCompiler.strcat(compiler)

    return compiler.types.set(Types.STRING)


def strmake(compiler, node):
    """ Компиляция built-in функции strmake (создание строки из n одинаковых символов) """
    node.args.elements[1].compile_asm(compiler)
    compiler.types.pop()
    node.args.elements[0].compile_asm(compiler)
    compiler.types.pop()
    StringCompiler.strmake(compiler)

    return compiler.types.set(Types.STRING)


def strcmp(compiler, node):
    """ Компиляция built-in функции strcmp (посимвольное сравнение двух строк) """
    node.args.elements[0].compile_asm(compiler)
    compiler.types.pop()
    node.args.elements[1].compile_asm(compiler)
    compiler.types.pop()
    StringCompiler.strcmp(compiler)

    return compiler.types.set(Types.INT)
