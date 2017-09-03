# -*- coding: utf-8 -*-

from src.Compiler.VM.Deep.strings import *

""" Мапа: арифметический оператор в языке программирования - арифметический оператор в коде стековой машины """
binop_compare_map = {
    '=': Add,
    '-': Sub,
    '*': Mul,
    '/': Div,
    '%': Mod
}

""" Компиляция арифметического выражения """
def binop_aexp(commands, env, op, left, right):
    left.compile_vm(commands, env)
    right.compile_vm(commands, env)

    commands.append(binop_compare_map[op])

""" Компиляция числа """
def int_aexp(commands, env, i):
    commands.add(Push, i)

""" Компиляция переменной """
def var_aexp(commands, env, name):
    commands.add(Load, Env.get_var(env, name))
