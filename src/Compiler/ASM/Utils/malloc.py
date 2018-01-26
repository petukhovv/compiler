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
        if self.compiler.environment.current is None:
            self.compiler.code.add(Commands.CALL, ['malloc'])
        else:
            self.compiler.code.add(Commands.PUSH, Registers.EAX)
            self.compiler.code.add(Commands.CALL, ['_malloc'])
