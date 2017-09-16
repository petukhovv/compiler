# -*- coding: utf-8 -*-

from commands import Commands
from environment import Environment

VM_COMMANDS_SEPARATOR = '\n'

""" Запуск компилятора в стековый код (точка входа) """
def compile_vm(ast):
    commands = Commands()
    ast.compile_vm(commands, Environment())

    return VM_COMMANDS_SEPARATOR.join(commands)
