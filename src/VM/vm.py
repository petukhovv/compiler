# -*- coding: utf-8 -*-

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