# -*- coding: utf-8 -*-

from src.Compiler.VM.Deep.strings import *

""" Компиляция выражения "символ" """
def char(commands, data, character, need_typify=True):
    commands.add(Push, ord(character))
    if need_typify:
        return commands.set_and_return_type(Types.CHAR)

""" Компиляция выражения "строка" """
def string(commands, data, characters):
    commands.add(Push, 0)
    for character in characters:
        char(commands, data, character, need_typify=False)

    commands.add(Push, len(characters))
    StringCompiler.store(commands, data)

    return commands.set_and_return_type(Types.STRING)

""" Компиляция built-in функции strlen (длина строки) """
def strlen(commands, data, args):
    array_type = args.elements[0].compile_vm(commands, data)
    commands.extract_value()

    StringCompiler.strlen(commands, data, array_type)

    return commands.set_and_return_type(Types.INT)

""" Компиляция built-in функции strget (получение символа строки) """
def strget(commands, data, args):
    # Порядок компиляции аргументов здесь и ниже задаём удобным для дальнейшей работы образом
    args.elements[1].compile_vm(commands, data)
    commands.extract_value()
    array_type = args.elements[0].compile_vm(commands, data)
    commands.extract_value()
    StringCompiler.strget(commands, data, array_type)

    return commands.set_and_return_type(Types.CHAR)

""" Компиляция built-in функции strset (задание символа строки) """
def strset(commands, data, args):
    args.elements[2].compile_vm(commands, data)
    commands.extract_value()
    args.elements[1].compile_vm(commands, data)
    commands.extract_value()
    array_type = args.elements[0].compile_vm(commands, data)
    commands.extract_value()
    StringCompiler.strset(commands, data, array_type)

""" Компиляция built-in функции strsub (взятие подстроки строки) """
def strsub(commands, data, args):
    args.elements[1].compile_vm(commands, data)
    commands.extract_value()
    array_type = args.elements[0].compile_vm(commands, data)
    commands.extract_value()
    args.elements[2].compile_vm(commands, data)
    commands.extract_value()
    StringCompiler.strsub(commands, data, array_type)

    return commands.set_and_return_type(Types.STRING)

""" Компиляция built-in функции strdup (дублирование строки) """
def strdup(commands, data, args):
    array_type = args.elements[0].compile_vm(commands, data)
    commands.extract_value()
    StringCompiler.strdup(commands, data, array_type)

    return commands.set_and_return_type(Types.STRING)

""" Компиляция built-in функции strcat (конкатенация двух строк) """
def strcat(commands, data, args):
    array_type1 = args.elements[0].compile_vm(commands, data)
    commands.extract_value()
    StringCompiler.strcat_first(commands, data, array_type1)
    array_type2 = args.elements[1].compile_vm(commands, data)
    commands.extract_value()
    StringCompiler.strcat_second(commands, data, array_type2)

    return commands.set_and_return_type(Types.STRING)

""" Компиляция built-in функции strmake (создание строки из n одинаковых символов) """
def strmake(commands, data, args):
    args.elements[1].compile_vm(commands, data)
    commands.extract_value()
    args.elements[0].compile_vm(commands, data)
    commands.extract_value()
    StringCompiler.strmake(commands, data)

    return commands.set_and_return_type(Types.STRING)

""" Компиляция built-in функции strcmp (посимвольное сравнение двух строк) """
def strcmp(commands, data, args):
    array_type2 = args.elements[0].compile_vm(commands, data)
    commands.extract_value()
    array_type1 = args.elements[1].compile_vm(commands, data)
    commands.extract_value()
    StringCompiler.strcmp(commands, data, array_type1, array_type2)

    return commands.set_and_return_type(Types.INT)
