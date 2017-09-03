# -*- coding: utf-8 -*-

from pprint import pprint

""" Compile-time environment """
class Env:
    """ Создание новой метки """
    @staticmethod
    def label(env, name=None):
        label_number = env['label_counter']
        if name:
            env['labels'][name] = label_number
        env['label_counter'] += 1
        return label_number

    """
    Создание новой переменной в stack memory
    Если name не передано, просто инкрементируем счетчик
    """
    @staticmethod
    def var(env, name=None):
        var_number = env['var_counter']
        # Если переменная уже существует, возвращаем её
        if Env.is_exist_var(env, name):
            return Env.get_var(env, name)
        if name is not None:
            env['vars'][name] = {'number': var_number}
        env['var_counter'] += 1
        return var_number

    """ Получение метки по имени """
    @staticmethod
    def get_label(env, name):
        return env['labels'][name]

    """ Получение переменной по имени """
    @staticmethod
    def get_var(env, name):
        return env['vars'][name]['number']

    """ Проверка переменной на существование """
    @staticmethod
    def is_exist_var(env, name):
        return name in env['vars']
