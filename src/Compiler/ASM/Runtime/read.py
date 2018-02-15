from ..Core.commands import Commands
from ..Core.registers import Registers
from ..Runtime.atoi import *

from .write import Write


class Read(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if Read.is_loaded:
            return

        self.load('read.asm', 'read')
        Read.is_loaded = True

        Write(compiler)

    def call(self):
        self.compiler.code.add(Commands.CALL, ['read'])

        Atoi(self.compiler)

        self.compiler.code.add(Commands.MOV, [Registers.EAX, 62])
        self.compiler.code.add(Commands.CALL, ['write'])
        self.compiler.code.add(Commands.MOV, [Registers.EAX, 32])
        self.compiler.code.add(Commands.CALL, ['write'])

        self.compiler.code.add(Commands.CALL, ['atoi'])
        self.compiler.code.add(Commands.PUSH, Registers.EAX)
