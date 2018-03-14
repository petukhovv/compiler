# -*- coding: utf-8 -*-


class Commands:
    """ Команды виртуальной машины """
    list = []       # Список команд
    current = 0     # Номер (индекс) текущей команды

    def __init__(self, commands_list):
        self.list = commands_list


class Scope:
    """ Область видимости """
    def __init__(self):
        self.stack = []     # Стековая память (static allocation data)


class VM:
    """ Виртуальная машина """
    root_scope = 'root'     # Название корневой области видимости

    def __init__(self, commands, initial_scope):
        self.labels = []                # Список меток
        self.scopes = [initial_scope]   # Стек областей видимости
        self.stack = []                 # Основной рабочий стек виртуальный машины
        self.heap = []                  # Куча (dynamic allocation data)
        self.call_stack = []            # Стек вызовов
        self.commands = commands        # Список комманд
        self.stack_memory_sizes = {}    # Мапа с областями видимости и требуемыми для них размерами стековой памяти

    def scope(self, index=-1):
        """ Получние текущей или указанной области видимости """
        return self.scopes[index]

    def create_scope(self, name=None):
        """ Создание области видимости и выделение для неё стековой памяти (если указан идентификатор) """
        self.scopes.append(Scope())
        if name is not None:
            self.allocate_stack_memory(name)
        return self.scope()

    def remove_scope(self):
        """ Удаление текущей области видимости """
        self.scopes.pop()

    def set_stack_memory_sizes(self, sizes):
        """ Установление мапы с областями видимости и требуемыми для них размерами стековой памяти """
        self.stack_memory_sizes = sizes

    def allocate_stack_memory(self, scope_name):
        """ Выделение стековой памяти под указанную область видимости """
        self.scope().stack = [None] * self.stack_memory_sizes[scope_name]

    def allocate_labels(self, size):
        """ Выделение памяти под метки """
        self.labels = [None] * size
