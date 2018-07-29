from ..Core.commands import Commands
from ..Runtime.base import Base


class Free(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if Free.is_loaded:
            return

        self.load('free.asm', 'free')
        Free.is_loaded = True

    def call(self):
        self.compiler.code.add(Commands.CALL, ['free'])
