# -*- coding: utf-8 -*-

""" Команды виртуальной машины """
class Commands:
    list = []       # Список команд
    current = 0     # Номер (индекс) текущей команды

    def __init__(self, commands_list):
        self.list = commands_list

""" Область видимости """
class Scope:
    def __init__(self):
        self.heap = []      # Куча (dynamic allocation data)
        self.stack = []     # Стековая память (static allocation data)

""" Виртуальная машина """
class VM:
    root_scope = 'root'     # Название корневой области видимости

    def __init__(self, commands, initial_scope):
        self.labels = []
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

    def allocate_labels(self, size):
        self.labels = [None] * size
