# -*- coding: utf-8 -*-

from src.Compiler.VM.Deep.strings import *

""" Компиляция выражения "символ" """
def char(commands, env, character, need_typify=True):
    commands.add(Push, ord(character))
    if need_typify:
        commands.typify(types.CHAR)

""" Компиляция выражения "строка" """
def string(commands, env, characters):
    # Записываем маркер конца строки
    commands.add(Push, 0)
    # Кладем на стек строку
    for character in characters:
        char(commands, env, character, need_typify=False)
    commands.add(Push, len(characters))

    # Записываем строку со стека в heap memory
    StringCompiler.store(commands, env)

    commands.typify(types.STRING)

""" Компиляция built-in функции strlen (длина строки) """
def strlen(commands, env, args):
    args_compile(args, 0, commands, env)
    commands.extract_value()
    StringCompiler.strlen(commands, env)

    commands.typify(types.INT)

""" Компиляция built-in функции strget (получение символа строки) """
def strget(commands, env, args):
    # Порядок компиляции аргументов здесь и ниже задаём удобным для дальнейшей работы образом
    args_compile(args, 1, commands, env)
    commands.extract_value()
    args_compile(args, 0, commands, env)
    commands.extract_value()
    StringCompiler.strget(commands, env)

    commands.typify(types.CHAR)

""" Компиляция built-in функции strset (задание символа строки) """
def strset(commands, env, args):
    args_compile(args, 2, commands, env)
    commands.extract_value()
    args_compile(args, 1, commands, env)
    commands.extract_value()
    args_compile(args, 0, commands, env)
    commands.extract_value()
    StringCompiler.strset(commands, env)

""" Компиляция built-in функции strsub (взятие подстроки строки) """
def strsub(commands, env, args):
    args_compile(args, 1, commands, env)
    commands.extract_value()
    args_compile(args, 0, commands, env)
    commands.extract_value()
    args_compile(args, 2, commands, env)
    commands.extract_value()
    StringCompiler.strsub(commands, env)

    commands.typify(types.STRING)

""" Компиляция built-in функции strdup (дублирование строки) """
def strdup(commands, env, args):
    args_compile(args, 0, commands, env)
    commands.extract_value()
    StringCompiler.strdup(commands, env)

    commands.typify(types.STRING)

""" Компиляция built-in функции strcat (конкатенация двух строк) """
def strcat(commands, env, args):
    args_compile(args, 0, commands, env)
    commands.extract_value()
    StringCompiler.strcat_first(commands, env)
    args_compile(args, 1, commands, env)
    commands.extract_value()
    StringCompiler.strcat_second(commands, env)

    commands.typify(types.STRING)

""" Компиляция built-in функции strmake (создание строки из n одинаковых символов) """
def strmake(commands, env, args):
    args_compile(args, 1, commands, env)
    commands.extract_value()
    args_compile(args, 0, commands, env)
    commands.extract_value()
    StringCompiler.strmake(commands, env)

    commands.typify(types.STRING)

""" Компиляция built-in функции strcmp (посимвольное сравнение двух строк) """
def strcmp(commands, env, args):
    args_compile(args, 0, commands, env)
    commands.extract_value()
    args_compile(args, 1, commands, env)
    commands.extract_value()
    StringCompiler.strcmp(commands, env)

    commands.typify(types.INT)
