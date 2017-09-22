# -*- coding: utf-8 -*-

from pprint import pprint

""" Команды виртуальной машины """
class Commands:
    list = []       # Список команд
    current = 0     # Номер (индекс) текущей команды

    def __init__(self, commands_list):
        self.list = commands_list

""" Область видимости """
class Scope:
    def __init__(self):
        self.stack = []     # Стековая память (static allocation data)

""" Виртуальная машина """
class VM:
    root_scope = 'root'     # Название корневой области видимости

    def __init__(self, commands, initial_scope):
        self.labels = []                # Список меток
        self.scopes = [initial_scope]   # Стек областей видимости
        self.stack = []                 # Основной рабочий стек виртуальный машины
        self.heap = []                  # Куча (dynamic allocation data)
        self.call_stack = []            # Стек вызовов
        self.commands = commands        # Список комманд
        self.stack_memory_sizes = {}    # Мапа с областями видимости и требуемыми для них размерами стековой памяти

    """ Получние текущей или указанной области видимости """
    def scope(self, index=-1):
        return self.scopes[index]

    """ Создание области видимости и выделение для неё стековой памяти (если указан идентификатор) """
    def create_scope(self, name=None):
        self.scopes.append(Scope())
        if name is not None:
            self.allocate_stack_memory(name)
        return self.scope()

    """ Удаление текущей области видимости """
    def remove_scope(self):
        self.scopes.pop()

    """ Установление мапы с областями видимости и требуемыми для них размерами стековой памяти """
    def set_stack_memory_sizes(self, sizes):
        self.stack_memory_sizes = sizes

    """ Выделение стековой памяти под указанную область видимости """
    def allocate_stack_memory(self, scope_name):
        self.scope().stack = [None] * self.stack_memory_sizes[scope_name]

    """ Выделение памяти под метки """
    def allocate_labels(self, size):
        self.labels = [None] * size
