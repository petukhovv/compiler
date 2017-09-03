# -*- coding: utf-8 -*-

from src.VM.Helpers.parser import command_class_relation_map, ARGS_SEPARATOR
from src.VM.commands import *

commands_relation_map = dict((command_class_relation_map[k], k) for k in command_class_relation_map)


class Commands(list):
    """ Добалвение команды в список команд для стековой машины """
    def add(self, command, argument=None):
        self.append(self.gen(command, argument))
        return self

    """ Генерация строкового представления заданной команды для стековой машины """
    @staticmethod
    def gen(command, argument=None):
        argument = '' if argument is None else ARGS_SEPARATOR + str(argument)
        return commands_relation_map[command] + argument
