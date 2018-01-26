from .code import Code
from .commands import Commands
from .environment import Environment
from .labels import Labels
from .registers import Registers
from .types import Types
from .vars import Vars
from .config import *


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

