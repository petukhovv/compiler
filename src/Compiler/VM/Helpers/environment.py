# -*- coding: utf-8 -*-

from pprint import pprint

""" Compile-time environment """
class Environment:
    var_counter = 1     # Счетчик переменных для stack memory
    vars = {}           # Переменные в stack memory
    label_counter = 1   # Счетчик меток
    labels = {}         # Метки

    current_function = None  # Тип данных возвращаемого значения из подпрограммы

    def set_return_type(self, type):
        if self.current_function is None:
            return

        self.labels[self.current_function]['return_type'] = type

    def get_return_type(self, name):
        return self.labels[name]['return_type']

    def start_function(self, name):
        start_function = self.label(name)
        self.current_function = name

        return start_function

    def finish_function(self):
        self.current_function = None

    """ Создание новой метки """
    def label(self, name=None):
        label_number = self.label_counter
        if name:
            self.labels[name] = {
                'number': label_number,
                'return_type': None
            }
        self.label_counter += 1
        return label_number

    """
    Создание новой переменной в stack memory
    Если name не передано, просто инкрементируем счетчик
    """
    def var(self, type=None, alias=None):
        var_number = self.var_counter
        # Если переменная уже существует, возвращаем её
        if self.is_exist_var(alias):
            return self.get_var(alias)
        if alias is not None:
            self.vars[alias] = {
                'number': var_number
            }
        self.vars[var_number] = {
            'type': type
        }
        if type:
            self.var_counter += 2
        else:
            self.var_counter += 1
        return var_number

    """ Получение метки по имени """
    def get_label(self, name):
        return self.labels[name]['number']

    """ Получение переменной по имени """
    def get_var(self, name):
        return self.vars[name]['number']

    """ Получение переменной по имени """
    def get_type(self, number):
        return self.vars[number]['type']

    """ Проверка переменной на существование """
    def is_exist_var(self, name):
        return name in self.vars
