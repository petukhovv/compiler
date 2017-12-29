from pprint import pprint

from .base import Base


class Itoa(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if Itoa.is_loaded:
            return

        self.load('itoa.asm')
        self.compiler.data.add('_itoa_radix', 'dd', '10')
        self.compiler.bss.add('_char', 'resb', 1)
        Itoa.is_loaded = True
