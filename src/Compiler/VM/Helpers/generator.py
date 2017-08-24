# -*- coding: utf-8 -*-

from src.VM.commands import *
from environment import Environment

"""
Генерация команд для организация цикла.
Цикл завершается, если на стеке оказалось 0.
После завершения на стек помещается число совершенных итераций.
"""
def cycle(commands, env, callback, load_counter=True):
    # Создаем метки и переменные, необходимые для прохождения цикла.
    start_while_label = Environment.create_label(env)
    end_while_label = Environment.create_label(env)
    counter_var = Environment.create_var(env)

    # Инициализируем счетчик цикла.
    commands.add(Push, 0)\
        .add(Store, counter_var)\
        .add(Label, start_while_label)

    # Выполняем тело цикла.
    callback(counter_var)

    # Инкрементируем счетчик цикла.
    commands.add(Load, counter_var)\
        .add(Push, 1)\
        .add(Add)\
        .add(Store, counter_var)\

    # Если после выполнения callback на стеке 0 - завершаем цикл.
    commands.add(Dup)\
        .add(Jz, end_while_label)\
        .add(Jump, start_while_label)\
        .add(Label, end_while_label)

    # Очищаем оставшийся на стеке 0 (поскольку перед Jz использовали Dup).
    commands.add(Pop)

    # Если требуется, загружаем на стек количество совершенных итераций.
    if load_counter:
        commands.add(Load, counter_var)
