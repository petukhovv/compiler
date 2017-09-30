from pprint import pprint

from base import Base
from ..Utils.atoi import *

class Read(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if self.is_loaded:
            return

        self.load('read.asm')
        self.compiler.bss.add('_read_buffer', 'resb', 255)
        self.compiler.data.add('_read_buffer_size', 'dd', '255')
        self.is_loaded = True

    def call(self):
        self.compiler.code.add('call', ['_read'])

        Atoi(self.compiler)
        self.compiler.code.add('mov', ['esi', '_read_buffer'])
        self.compiler.code.add('mov', ['eax', 0])
        self.compiler.code.add('call', ['_atoi'])
        self.compiler.code.add('push', ['eax'])
