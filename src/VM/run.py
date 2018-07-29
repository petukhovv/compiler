# -*- coding: utf-8 -*-

from .commands import Label, Function, Store, Return, BStore
from .vm import Commands, Scope, VM


def run(commands_list):
    """ Запуск виртуальной машины """
    commands = Commands(commands_list)
    vm = VM(commands, Scope())

    current_scope = VM.root_scope
    stack_memory_sizes = {current_scope: 0}

    # Подсчет количества меток и выделение памяти для их хранения
    labels_count = sum(isinstance(x, Label) for x in commands.list)
    vm.allocate_labels(labels_count)

    # Первый проход:
    #   1) Находим метки и записываем в соответствующее хранилище виртуальной машины
    #   2) Конструируем мапу с областями видимости и требуемыми для них размерами стековой памяти
    #       2.1) По умолчанию инкрементируем требуемый размер для корневой обалсти видимости
    #       2.2) При входе в функцию начинаем инкрементировать требуемый размер для её обалсти видимости
    #       2.3) При выходе из функции продолжаем работать с корневой областью видимостью
    while commands.current < len(commands.list):
        command = commands.list[commands.current]
        if isinstance(command, Label):
            command.interpret(vm)
        if isinstance(command, Function):
            current_scope = command.name
            stack_memory_sizes[current_scope] = 0
        if isinstance(command, Return):
            current_scope = VM.root_scope
        if isinstance(command, Store) or isinstance(command, BStore):
            stack_memory_sizes[current_scope] += 1
        commands.current += 1
    commands.current = 0

    vm.set_stack_memory_sizes(stack_memory_sizes)
    # Выделяем стековую память для корневой области видимости
    vm.allocate_stack_memory(VM.root_scope)

    # Второй проход: выполняем программу (интерпретируем стековый код)
    while commands.current < len(commands.list):
        command = commands.list[commands.current]
        if not isinstance(command, Label):
            command.interpret(vm)
        commands.current += 1
    commands.current = 0
