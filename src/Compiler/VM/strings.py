# -*- coding: utf-8 -*-

from src.Compiler.VM.Deep.strings import *

""" Компиляция выражения "символ" """
def char(commands, data, character, need_typify=True):
    commands.add(Push, ord(character))
    if need_typify:
        return commands.set_and_return_type(types.CHAR)

""" Компиляция выражения "строка" """
def string(commands, data, characters):
    # Записываем маркер конца строки
    commands.add(Push, 0)
    # Кладем на стек строку
    for character in characters:
        char(commands, data, character, need_typify=False)
    commands.add(Push, len(characters))

    # Записываем строку со стека в heap memory
    StringCompiler.store(commands, data)

    return commands.set_and_return_type(types.STRING)

""" Компиляция built-in функции strlen (длина строки) """
def strlen(commands, data, args):
    args_compile(args, 0, commands, data)
    commands.extract_value()
    StringCompiler.strlen(commands, data)

    return commands.set_and_return_type(types.INT)

""" Компиляция built-in функции strget (получение символа строки) """
def strget(commands, data, args):
    # Порядок компиляции аргументов здесь и ниже задаём удобным для дальнейшей работы образом
    args_compile(args, 1, commands, data)
    commands.extract_value()
    args_compile(args, 0, commands, data)
    commands.extract_value()
    StringCompiler.strget(commands, data)

    return commands.set_and_return_type(types.CHAR)

""" Компиляция built-in функции strset (задание символа строки) """
def strset(commands, data, args):
    args_compile(args, 2, commands, data)
    commands.extract_value()
    args_compile(args, 1, commands, data)
    commands.extract_value()
    args_compile(args, 0, commands, data)
    commands.extract_value()
    StringCompiler.strset(commands, data)

""" Компиляция built-in функции strsub (взятие подстроки строки) """
def strsub(commands, data, args):
    args_compile(args, 1, commands, data)
    commands.extract_value()
    args_compile(args, 0, commands, data)
    commands.extract_value()
    args_compile(args, 2, commands, data)
    commands.extract_value()
    StringCompiler.strsub(commands, data)

    return commands.set_and_return_type(types.STRING)

""" Компиляция built-in функции strdup (дублирование строки) """
def strdup(commands, data, args):
    args_compile(args, 0, commands, data)
    commands.extract_value()
    StringCompiler.strdup(commands, data)

    return commands.set_and_return_type(types.STRING)

""" Компиляция built-in функции strcat (конкатенация двух строк) """
def strcat(commands, data, args):
    args_compile(args, 0, commands, data)
    commands.extract_value()
    StringCompiler.strcat_first(commands, data)
    args_compile(args, 1, commands, data)
    commands.extract_value()
    StringCompiler.strcat_second(commands, data)

    return commands.set_and_return_type(types.STRING)

""" Компиляция built-in функции strmake (создание строки из n одинаковых символов) """
def strmake(commands, data, args):
    args_compile(args, 1, commands, data)
    commands.extract_value()
    args_compile(args, 0, commands, data)
    commands.extract_value()
    StringCompiler.strmake(commands, data)

    return commands.set_and_return_type(types.STRING)

""" Компиляция built-in функции strcmp (посимвольное сравнение двух строк) """
def strcmp(commands, data, args):
    args_compile(args, 0, commands, data)
    commands.extract_value()
    args_compile(args, 1, commands, data)
    commands.extract_value()
    StringCompiler.strcmp(commands, data)

    return commands.set_and_return_type(types.INT)
