# -*- coding: utf-8 -*-

from src.VM.commands import *

from Helpers.env import *

""" Мапа: оператор сравнения в языке программирования - оператор сравнения в коде стековой машины """
relop_compare_map = {
    '==':   0,
    '!=':   1,
    '<':    2,
    '>':    3,
    '<=':   4,
    '>=':   5
}

""" Компиляция операторов сравнения """
def relop_bexp(commands, env, op, left, right):
    left.compile_vm(commands, env)
    right.compile_vm(commands, env)

    commands.add(Compare, relop_compare_map[op])

""" Компиляция оператора логического "И" (and) """
def and_bexp(commands, env, left, right):
    finish_label = Env.label(env)
    finish_false_label = Env.label(env)

    left.compile_vm(commands, env)
    commands.add(Push, 0)\
        .add(Compare, 0)

    # Если первый операнд == 0, второй уже не проверяем,
    # а сразу переходим к метке ложного результата (ленивая проверка)
    commands.add(Jnz, finish_false_label)

    # Иначе будем проверять и второй
    right.compile_vm(commands, env)
    commands.add(Push, 0)\
        .add(Compare, 0)

    # Если второй операнд == 0, то переходим к метке ложного результата
    commands.add(Jnz, finish_false_label)

    # Если оба операнда == 1, то в целом результат выполнения and - 1 - его и пишем в стек
    # и переходим к метке полного завершения выполнения and (минуя секцию ложного результата).
    commands.add(Push, 1)\
        .add(Jump, finish_label)

    # Секция ложного результата, пишем в стек 0
    commands.add(Label, finish_false_label)\
        .add(Push, 0)

    # Полное завершения выполнения and
    commands.add(Label, finish_label)

""" Компиляция оператора логического "ИЛИ" (or) """
def or_bexp(commands, env, left, right):
    finish_label = Env.label(env)
    finish_true_label = Env.label(env)

    left.compile_vm(commands, env)
    commands.add(Push, 0)\
        .add(Compare, 1)

    # Если первый операнд != 0, второй уже не проверяем,
    # а сразу переходим к метке истинного результата (ленивая проверка)
    commands.add(Jnz, finish_true_label)

    # Иначе будем проверять и второй
    right.compile_vm(commands, env)
    commands.add(Push, 0)\
        .add(Compare, 1)

    # Если второй операнд != 0, то переходим к метке истинного результата
    commands.add(Jnz, finish_true_label)

    # Если оба операнда = 0, то в целом результат выполнения or - 0 - его и пишем в стек
    # и переходим к метке полного завершения выполнения or (минуя секцию истинного результата)
    commands.add(Push, 0)\
        .add(Jump, finish_label)

    # Секция истинного результата, пишем в стек 1
    commands.add(Label, finish_true_label)\
        .add(Push, 1)

    # Полное завершения выполнения or
    commands.add(Label, finish_label)

""" Компиляция оператора логического "НЕ" (not) """
def not_bexp(commands, env, exp):
    finish_label = Env.label(env)
    finish_false_label = Env.label(env)

    exp.compile_vm(commands, env)
    commands.add(Push, 0)\
        .add(Compare, 0)

    # Если операнд == 0, переходим в секцию ложного результата
    commands.add(Jnz, finish_false_label)

    # Секция истинного результата, пишем в стек 1
    commands.add(Push, 1)\
        .add(Jump, finish_label)

    # Секция ложного результата, пишем в стек 0
    commands.add(Label, finish_false_label)\
        .add(Push, 0)

    # Полное завершения выполнения оператора not
    commands.add(Label, finish_label)
