# -*- coding: utf-8 -*-

from ..Config.general import *

from .environment import Environment
from .types import Types
from .labels import Labels
from .vars import Vars
from .commands import Commands
from .registers import Registers


class Code(list):
    stack_balance = 0

    def check_and_fix_stack_balance(self):
        if self.stack_balance != 0:
            for i in range(1, self.stack_balance):
                self.add(Commands.ADD, [Registers.ESP, 4])
                self.stack_balance -= 1

    def stack_pop(self):
        self.stack_balance -= 1
        self.add(Commands.ADD, [Registers.ESP, 4])

    def add(self, command, args):
        if command == Commands.PUSH:
            self.stack_balance += 1
        elif command == Commands.POP:
            self.stack_balance -= 1

        self.append(command + '\t\t' + ASM_ARGS_SEPARATOR.join(str(x) for x in args))


class Compiler:
    def __init__(self):
        self.environment = Environment()
        self.code = Code()
        self.labels = Labels()
        self.vars = Vars(self, self.code, self.environment)
        self.types = Types(self)
        self.target_register = None

    def exit(self):
        self.code.add(Commands.PUSH, [0])
        self.code.add(Commands.MOV, [Registers.EAX, 1])
        self.code.add(Commands.SUB, [Registers.ESP, 1])
        self.code.add(Commands.INT, [0x80])

    def get_result(self):
        self.exit()

        return (
            'EXTERN _malloc' + ASM_COMMANDS_SEPARATOR +
            'SECTION .data' + ASM_COMMANDS_SEPARATOR +
            ASM_COMMANDS_SEPARATOR.join(self.vars.data) +
            'SECTION .bss' + ASM_COMMANDS_SEPARATOR +
            ASM_COMMANDS_SEPARATOR.join(self.vars.bss) +
            'SECTION .text' + ASM_COMMANDS_SEPARATOR +
            'global _main' + ASM_COMMANDS_SEPARATOR +
            ASM_COMMANDS_SEPARATOR.join(self.labels) + ASM_COMMANDS_SEPARATOR +
            '_main:' + ASM_COMMANDS_SEPARATOR +
            ASM_COMMANDS_SEPARATOR.join(self.code) + ASM_COMMANDS_SEPARATOR
        )


def compile_asm(ast):
    """ Запуск компилятора в код языка ассемблера NASM (x86) """
    compiler = Compiler()

    ast.compile_asm(compiler)

    return compiler.get_result()
