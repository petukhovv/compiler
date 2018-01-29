from ..Core.commands import Commands
from ..Core.registers import Registers
from ..Utils.atoi import *


class Malloc(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if Malloc.is_loaded:
            return

        self.load('malloc.asm')
        Malloc.is_loaded = True

    def call(self):
        self.compiler.code.add(Commands.MOV, [Registers.ECX, Registers.EAX])
        self.compiler.code.stack_align(16, 0)   # 4 - compensation of one argument push - memory size
        self.compiler.code.add(Commands.PUSH, Registers.ECX)
        self.compiler.code.add(Commands.CALL, ['_malloc'])
        self.compiler.code.add(Commands.ADD, [Registers.ESP, 4])
        self.compiler.code.restore_stack_align()
