# -*- coding: utf-8 -*-

from Helpers.base import *
from src.VM.commands import *

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
    commands.extract_value()
    right.compile_vm(commands, env)
    commands.extract_value()

    commands.add(Compare, relop_compare_map[op])

    commands.typify(types.INT)

""" Компиляция оператора логического "И" (and) """
def and_bexp(commands, env, left, right):
    finish_label = env.label()
    finish_false_label = env.label()

    left.compile_vm(commands, env)
    commands.extract_value()

    # Если первый операнд == 0, второй уже не проверяем,
    # а сразу переходим к метке ложного результата (ленивая проверка)
    commands.add(Jz, finish_false_label)

    # Иначе будем проверять и второй
    right.compile_vm(commands, env)
    commands.extract_value()

    # Если второй операнд == 0, то переходим к метке ложного результата
    commands.add(Jz, finish_false_label)

    # Если оба операнда == 1, то в целом результат выполнения and - 1 - его и пишем в стек
    # и переходим к метке полного завершения выполнения and (минуя секцию ложного результата).
    commands.push_value(1, types.BOOL)
    commands.add(Jump, finish_label)

    # Секция ложного результата, пишем в стек 0
    commands.add(Label, finish_false_label)
    commands.push_value(0, types.BOOL)

    # Полное завершения выполнения and
    commands.add(Label, finish_label)

""" Компиляция оператора логического "ИЛИ" (or) """
def or_bexp(commands, env, left, right):
    finish_label = env.label()
    finish_true_label = env.label()

    left.compile_vm(commands, env)
    commands.extract_value()

    # Если первый операнд != 0, второй уже не проверяем,
    # а сразу переходим к метке истинного результата (ленивая проверка)
    commands.add(Jnz, finish_true_label)

    # Иначе будем проверять и второй
    right.compile_vm(commands, env)
    commands.extract_value()

    # Если второй операнд != 0, то переходим к метке истинного результата
    commands.add(Jnz, finish_true_label)

    # Если оба операнда = 0, то в целом результат выполнения or - 0 - его и пишем в стек
    # и переходим к метке полного завершения выполнения or (минуя секцию истинного результата)
    commands.push_value(0, types.BOOL)
    commands.add(Jump, finish_label)

    # Секция истинного результата, пишем в стек 1
    commands.add(Label, finish_true_label)
    commands.push_value(1, types.BOOL)

    # Полное завершения выполнения or
    commands.add(Label, finish_label)

""" Компиляция оператора логического "НЕ" (not) """
def not_bexp(commands, env, exp):
    finish_label = env.label()
    finish_false_label = env.label()

    exp.compile_vm(commands, env)
    commands.extract_value()

    # Если операнд == 0, переходим в секцию ложного результата
    commands.add(Jnz, finish_false_label)

    # Секция истинного результата, пишем в стек 1
    commands.push_value(1, types.BOOL)
    commands.add(Jump, finish_label)

    # Секция ложного результата, пишем в стек 0
    commands.add(Label, finish_false_label)
    commands.push_value(0, types.BOOL)

    # Полное завершения выполнения оператора not
    commands.add(Label, finish_label)
