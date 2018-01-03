from ..Helpers.types import *

from .base import Base
from .itoa import Itoa


class Write(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if Write.is_loaded:
            return

        self.load('write.asm')
        Write.is_loaded = True

    def call(self, value_type):
        if value_type == Types.INT or True:
            Itoa(self.compiler)
            self.compiler.code.add('pop', ['eax'])
            self.compiler.code.add('call', ['_itoa'])
            self.compiler.code.add('mov', ['eax', 10])
            self.compiler.code.add('call', ['_write'])
        else:
            pass
