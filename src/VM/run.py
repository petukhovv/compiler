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
        self.stack = {}  # Стековая память (static allocation data)
        self.heap = []  # Куча (dynamic allocation data)

class VM:
    def __init__(self, commands, initial_scope):
        self.labels = {}
        self.scopes = [initial_scope]
        self.stack = []
        self.call_stack = []
        self.commands = commands

    def scope(self, index=-1):
        return self.scopes[index]

    def create_scope(self):
        self.scopes.append(Scope())
        return self.scope()

    def remove_scope(self):
        self.scopes.pop()

def interpret(commands_list):
    commands = Commands(commands_list)
    vm = VM(commands, Scope())

    # Первый проход: находим метки и заносим их в runtime-environment
    while commands.current < len(commands.list):
        command_class = commands.list[commands.current]
        if isinstance(command_class, Label):
            command_class.eval(vm)
        commands.current += 1
    commands.current = 0

    # Второй проход: выполняем программу
    while commands.current < len(commands.list):
        command_class = commands.list[commands.current]
        if not isinstance(command_class, Label):
            command_class.eval(vm)
        commands.current += 1
    commands.current = 0
