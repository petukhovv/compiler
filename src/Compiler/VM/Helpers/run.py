# -*- coding: utf-8 -*-

from src.VM.Helpers.parser import COMMAND_SEPARATOR as VM_COMMANDS_SEPARATOR
from assembler import Commands

""" Запуск компилятора в стековый код (точка входа) """
def compile_vm(ast):
    commands = Commands()

    ast.compile_vm(commands, {
        'var_counter': 1,       # Счетчик переменных для stack memory
        'vars': {},             # Переменные в stack memory
        'label_counter': 1,     # Счетчик меток
        'labels': {}            # Метки
    })

    return VM_COMMANDS_SEPARATOR.join(commands)
