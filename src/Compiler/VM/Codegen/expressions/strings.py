# -*- coding: utf-8 -*-

from ...Deep.strings import StringCompiler
from ...Helpers.types import Types
from ...Helpers.commands import Push


def char(commands, data, node):
    """ Компиляция выражения "символ" """
    commands.add(Push, ord(node.character))

    return commands.set_and_return_type(Types.CHAR)


def string(commands, data, node):
    """ Компиляция выражения "строка" """
    commands.add(Push, 0)
    for character in node.characters:
        commands.add(Push, ord(character))

    commands.add(Push, len(node.characters))
    StringCompiler.store(commands, data)

    return commands.set_and_return_type(Types.STRING)


def strlen(commands, data, node):
    """ Компиляция built-in функции strlen (длина строки) """
    array_type = node.args.elements[0].compile_vm(commands, data)
    commands.clean_type()

    StringCompiler.strlen(commands, data, array_type)

    return commands.set_and_return_type(Types.INT)


def strget(commands, data, node):
    """ Компиляция built-in функции strget (получение символа строки) """
    # Порядок компиляции аргументов здесь и ниже задаём удобным для дальнейшей работы образом
    node.args.elements[1].compile_vm(commands, data)
    commands.clean_type()
    array_type = node.args.elements[0].compile_vm(commands, data)
    commands.clean_type()
    StringCompiler.strget(commands, data, array_type)

    return commands.set_and_return_type(Types.CHAR)


def strsub(commands, data, node):
    """ Компиляция built-in функции strsub (взятие подстроки строки) """
    node.args.elements[1].compile_vm(commands, data)
    commands.clean_type()
    array_type = node.args.elements[0].compile_vm(commands, data)
    commands.clean_type()
    node.args.elements[2].compile_vm(commands, data)
    commands.clean_type()
    StringCompiler.strsub(commands, data, array_type)

    return commands.set_and_return_type(Types.STRING)


def strdup(commands, data, node):
    """ Компиляция built-in функции strdup (дублирование строки) """
    array_type = node.args.elements[0].compile_vm(commands, data)
    commands.clean_type()
    StringCompiler.strdup(commands, data, array_type)

    return commands.set_and_return_type(Types.STRING)


def strcat(commands, data, node):
    """ Компиляция built-in функции strcat (конкатенация двух строк) """
    array_type1 = node.args.elements[0].compile_vm(commands, data)
    commands.clean_type()
    StringCompiler.strcat_first(commands, data, array_type1)
    array_type2 = node.args.elements[1].compile_vm(commands, data)
    commands.clean_type()
    StringCompiler.strcat_second(commands, data, array_type2)

    return commands.set_and_return_type(Types.STRING)


def strmake(commands, data, node):
    """ Компиляция built-in функции strmake (создание строки из n одинаковых символов) """
    node.args.elements[1].compile_vm(commands, data)
    commands.clean_type()
    node.args.elements[0].compile_vm(commands, data)
    commands.clean_type()
    StringCompiler.strmake(commands, data)

    return commands.set_and_return_type(Types.STRING)


def strcmp(commands, data, node):
    """ Компиляция built-in функции strcmp (посимвольное сравнение двух строк) """
    array_type2 = node.args.elements[0].compile_vm(commands, data)
    commands.clean_type()
    array_type1 = node.args.elements[1].compile_vm(commands, data)
    commands.clean_type()
    StringCompiler.strcmp(commands, data, array_type1, array_type2)

    return commands.set_and_return_type(Types.INT)
