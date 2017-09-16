# -*- coding: utf-8 -*-

from conf import *
from pprint import pprint

# Парсинг программы в стековом коде (преобразование в список команд): простой split строк
def parse(program):
    commands = program.split(COMMAND_SEPARATOR)
    command_classes = []
    for command in commands:
        command = command.split(ARGS_SEPARATOR)
        args = []
        for arg in command[1:]:
            args.append(int(arg))
        command_classes.append(commands_map[command[0]](*args))

    return command_classes
