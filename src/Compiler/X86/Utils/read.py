from pprint import pprint

from base import Base

class Read(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if self.is_loaded:
            return

        self.load('read.asm')
        self.compiler.bss.add('_read_buffer', 'resb', 255)
        self.compiler.bss.add('_read_buffer_size', 'resb', 255)
        self.is_loaded = True

    def call(self):
        self.compiler.code.add('call', ['_read'])
