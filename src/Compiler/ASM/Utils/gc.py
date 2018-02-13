from ..Core.types import Types
from ..Core.commands import Commands
from ..Core.registers import Registers
from ..Utils.atoi import *


class GC(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if GC.is_loaded:
            return

        self.load('gc.asm')
        GC.is_loaded = True

    def run(self):
        self.compiler.code.add(Commands.CALL, ['gc'])

    def increment(self):
        self.compiler.code.add(Commands.CALL, ['gc.gc_increment'])
