# -*- coding: utf-8 -*-

from .conf import COMMAND_SEPARATOR, ARGS_SEPARATOR, commands_map


def parse(program):
    """ Парсинг программы в стековом коде (преобразование в список команд): простой split строк """
    commands = program.split(COMMAND_SEPARATOR)
    command_classes = []
    for command in commands:
        command = command.split(ARGS_SEPARATOR)
        args = []
        for arg in command[1:]:
            args.append(int(arg))
        command_classes.append(commands_map[command[0]](*args))

    return command_classes
