from .base import Base

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
        if self.compiler.environment.current_function is None:
            self.compiler.code.add('call', ['malloc'])
        else:
            self.compiler.code.add('push', ['eax'])
            self.compiler.code.add('call', ['_malloc'])
