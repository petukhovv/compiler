# -*- coding: utf-8 -*-

from pprint import pprint
from src.VM.commands import *
from vm import *

def run(commands_list):
    commands = Commands(commands_list)
    vm = VM(commands, Scope())

    current_scope = VM.root_scope
    stack_memory_sizes = {current_scope: 0}

    # Первый проход: находим метки и заносим их в runtime-environment
    while commands.current < len(commands.list):
        command_class = commands.list[commands.current]
        if isinstance(command_class, Label):
            command_class.eval(vm)
        if isinstance(command_class, Function):
            current_scope = command_class.name
            stack_memory_sizes[current_scope] = 0
        if isinstance(command_class, Return):
            current_scope = VM.root_scope
        if isinstance(command_class, Store) or isinstance(command_class, BStore):
            stack_memory_sizes[current_scope] += 1
        commands.current += 1
    commands.current = 0

    vm.set_stack_memory_sizes(stack_memory_sizes)
    vm.allocate_stack_memory(VM.root_scope)

    # Второй проход: выполняем программу
    while commands.current < len(commands.list):
        command_class = commands.list[commands.current]
        if not isinstance(command_class, Label):
            command_class.eval(vm)
        commands.current += 1
    commands.current = 0
