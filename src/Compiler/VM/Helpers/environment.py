# -*- coding: utf-8 -*-

from pprint import pprint

""" Compile-time environment """
class Environment:
    var_counter = 1     # Счетчик переменных для stack memory
    vars = {}           # Переменные в stack memory
    label_counter = 1   # Счетчик меток
    labels = {}         # Метки

    """ Создание новой метки """
    def label(self, name=None):
        label_number = self.label_counter
        if name:
            self.labels[name] = label_number
        self.label_counter += 1
        return label_number

    """
    Создание новой переменной в stack memory
    Если name не передано, просто инкрементируем счетчик
    """
    def var(self, name=None):
        var_number = self.var_counter
        # Если переменная уже существует, возвращаем её
        if self.is_exist_var(name):
            return self.get_var(name)
        if name is not None:
            self.vars[name] = {'number': var_number}
        self.var_counter += 1
        return var_number

    """ Получение метки по имени """
    def get_label(self, name):
        return self.labels[name]

    """ Получение переменной по имени """
    def get_var(self, name):
        return self.vars[name]['number']

    """ Проверка переменной на существование """
    def is_exist_var(self, name):
        return name in self.vars
