# -*- coding: utf-8 -*-

from pprint import pprint
from src.VM.commands import *

""" Память данных виртуальной машины """
data = {
    'variables': {},
    'labels': {},
    'call_stack': [],
    'environments': []
}

""" Стек виртуальной машины """
stack = []

def interpret(commands_list):
    commands = {
        'list': commands_list,
        'current': 0
    }

    # Первый проход: находим метки и заносим их в runtime-environment
    while commands['current'] < len(commands['list']):
        command_class = commands['list'][commands['current']]
        if isinstance(command_class, Label):
            command_class.eval(commands, data, stack)
        commands['current'] += 1
    commands['current'] = 0

    # Второй проход: выполняем программу
    while commands['current'] < len(commands['list']):
        command_class = commands['list'][commands['current']]
        if not isinstance(command_class, Label):
            command_class.eval(commands, data, stack)
        commands['current'] += 1
    commands['current'] = 0

    pprint(stack)
