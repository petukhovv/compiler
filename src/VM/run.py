# -*- coding: utf-8 -*-

from pprint import pprint
from src.VM.commands import *

class Commands:
    list = []
    current = 0

    def __init__(self, list):
        self.list = list

class Scope:
    def __init__(self):
        self.heap = []  # Куча (dynamic allocation data)
        self.stack = []  # Стековая память (static allocation data)

class VM:
    root_scope = 'root'

    def __init__(self, commands, initial_scope):
        self.labels = {}
        self.scopes = [initial_scope]
        self.stack = []
        self.call_stack = []
        self.commands = commands
        self.stack_memory_sizes = {}

    def scope(self, index=-1):
        return self.scopes[index]

    def create_scope(self, name=None):
        self.scopes.append(Scope())
        if name is not None:
            self.allocate_stack_memory(name)
        return self.scope()

    def remove_scope(self):
        self.scopes.pop()

    def set_stack_memory_sizes(self, sizes):
        self.stack_memory_sizes = sizes

    def allocate_stack_memory(self, scope_name):
        self.scope().stack = [None] * self.stack_memory_sizes[scope_name]

def interpret(commands_list):
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
