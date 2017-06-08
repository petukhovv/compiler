# -*- coding: utf-8 -*-

from pprint import pprint

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
    while commands['current'] < len(commands['list']):
        commands['list'][commands['current']].eval(commands, data, stack)
        pprint(commands['current'])
        commands['current'] += 1

    pprint(stack)
    pprint(data)
