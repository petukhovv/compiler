# -*- coding: utf-8 -*-

from Helpers.string import *
from Helpers.base import *

AST = sys.modules['src.Parser.AST.strings']

""" Компиляция выражения "символ" """
def char(commands, env, character):
    commands.add(Push, ord(character))

""" Компиляция выражения "строка" """
def string(commands, env, characters):
    # Записываем маркер конца строки
    commands.add(Push, 0)
    # Кладем на стек строку
    for character in characters:
        char(commands, env, character)
    commands.add(Push, len(characters))

    # Записываем строку со стека в heap memory
    StringCompiler.store(commands, env)

""" Компиляция built-in функции strlen (длина строки) """
def strlen(commands, env, args):
    args_compile(args, 0, commands, env)
    StringCompiler.strlen(commands, env)

""" Компиляция built-in функции strget (получение символа строки) """
def strget(commands, env, args):
    # Порядок компиляции аргументов здесь и ниже задаём удобным для дальнейшей работы образом
    args_compile(args, [1, 0], commands, env)
    StringCompiler.strget(commands, env)

""" Компиляция built-in функции strset (задание символа строки) """
def strset(commands, env, args):
    args_compile(args, [2, 1, 0], commands, env)
    StringCompiler.strset(commands, env)

""" Компиляция built-in функции strsub (взятие подстроки строки) """
def strsub(commands, env, args):
    args_compile(args, [1, 0, 2], commands, env)
    StringCompiler.strsub(commands, env)

""" Компиляция built-in функции strdup (дублирование строки) """
def strdup(commands, env, args):
    args_compile(args, 0, commands, env)
    StringCompiler.strdup(commands, env)

""" Компиляция built-in функции strcat (конкатенация двух строк) """
def strcat(commands, env, args):
    args_compile(args, 0, commands, env)
    StringCompiler.strcat(commands, env)
    args_compile(args, 1, commands, env)
    StringCompiler.strcat_join(commands, env)

""" Компиляция built-in функции strmake (создание строки из n одинаковых символов) """
def strmake(commands, env, args):
    args_compile(args, [1, 0], commands, env)
    StringCompiler.strmake(commands, env)

""" Компиляция built-in функции strcmp (посимвольное сравнение двух строк) """
def strcmp(commands, env, args):
    args_compile(args, [0, 1], commands, env)
    StringCompiler.strcmp(commands, env)
