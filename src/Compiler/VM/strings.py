# -*- coding: utf-8 -*-

from .Deep.strings import *


def char(commands, data, character, need_typify=True):
    """ Компиляция выражения "символ" """
    commands.add(Push, ord(character))
    if need_typify:
        return commands.set_and_return_type(Types.CHAR)


def string(commands, data, characters):
    """ Компиляция выражения "строка" """
    commands.add(Push, 0)
    for character in characters:
        char(commands, data, character, need_typify=False)

    commands.add(Push, len(characters))
    StringCompiler.store(commands, data)

    return commands.set_and_return_type(Types.STRING)


def strlen(commands, data, args):
    """ Компиляция built-in функции strlen (длина строки) """
    array_type = args.elements[0].compile_vm(commands, data)
    commands.extract_value()

    StringCompiler.strlen(commands, data, array_type)

    return commands.set_and_return_type(Types.INT)


def strget(commands, data, args):
    """ Компиляция built-in функции strget (получение символа строки) """
    # Порядок компиляции аргументов здесь и ниже задаём удобным для дальнейшей работы образом
    args.elements[1].compile_vm(commands, data)
    commands.extract_value()
    array_type = args.elements[0].compile_vm(commands, data)
    commands.extract_value()
    StringCompiler.strget(commands, data, array_type)

    return commands.set_and_return_type(Types.CHAR)


def strset(commands, data, args):
    """ Компиляция built-in функции strset (задание символа строки) """
    args.elements[2].compile_vm(commands, data)
    commands.extract_value()
    args.elements[1].compile_vm(commands, data)
    commands.extract_value()
    array_type = args.elements[0].compile_vm(commands, data)
    commands.extract_value()
    StringCompiler.strset(commands, data, array_type)


def strsub(commands, data, args):
    """ Компиляция built-in функции strsub (взятие подстроки строки) """
    args.elements[1].compile_vm(commands, data)
    commands.extract_value()
    array_type = args.elements[0].compile_vm(commands, data)
    commands.extract_value()
    args.elements[2].compile_vm(commands, data)
    commands.extract_value()
    StringCompiler.strsub(commands, data, array_type)

    return commands.set_and_return_type(Types.STRING)


def strdup(commands, data, args):
    """ Компиляция built-in функции strdup (дублирование строки) """
    array_type = args.elements[0].compile_vm(commands, data)
    commands.extract_value()
    StringCompiler.strdup(commands, data, array_type)

    return commands.set_and_return_type(Types.STRING)


def strcat(commands, data, args):
    """ Компиляция built-in функции strcat (конкатенация двух строк) """
    array_type1 = args.elements[0].compile_vm(commands, data)
    commands.extract_value()
    StringCompiler.strcat_first(commands, data, array_type1)
    array_type2 = args.elements[1].compile_vm(commands, data)
    commands.extract_value()
    StringCompiler.strcat_second(commands, data, array_type2)

    return commands.set_and_return_type(Types.STRING)


def strmake(commands, data, args):
    """ Компиляция built-in функции strmake (создание строки из n одинаковых символов) """
    args.elements[1].compile_vm(commands, data)
    commands.extract_value()
    args.elements[0].compile_vm(commands, data)
    commands.extract_value()
    StringCompiler.strmake(commands, data)

    return commands.set_and_return_type(Types.STRING)


def strcmp(commands, data, args):
    """ Компиляция built-in функции strcmp (посимвольное сравнение двух строк) """
    array_type2 = args.elements[0].compile_vm(commands, data)
    commands.extract_value()
    array_type1 = args.elements[1].compile_vm(commands, data)
    commands.extract_value()
    StringCompiler.strcmp(commands, data, array_type1, array_type2)

    return commands.set_and_return_type(Types.INT)
