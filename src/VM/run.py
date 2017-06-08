# -*- coding: utf-8 -*-

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
    commands.eval(commands, data, stack)
    pass