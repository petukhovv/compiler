# -*- coding: utf-8 -*-

from .commands import Commands
from .environment import Environment


VM_COMMANDS_SEPARATOR = '\n'


def compile_vm(ast):
    """ Запуск компилятора в стековый код (точка входа) """
    commands = Commands()
    ast.compile_vm(commands, Environment())

    return VM_COMMANDS_SEPARATOR.join(commands)
