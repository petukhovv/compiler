from ..Core.commands import Commands
from ..Runtime.base import Base


class Malloc(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if Malloc.is_loaded:
            return

        self.load('malloc.asm', 'malloc')
        Malloc.is_loaded = True

    def call(self):
        self.compiler.code.add(Commands.CALL, ['malloc'])
