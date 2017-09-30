from pprint import pprint
import os

from base import Base

class Itoa(Base):
    is_loaded = False

    def __init__(self, compiler):
        self.compiler = compiler

        if self.is_loaded:
            return

        dir = os.path.dirname(os.path.abspath(__file__))
        f = open(dir + self.path + 'itoa.asm', 'r')
        itoa_code = f.read()
        self.compiler.labels.add(itoa_code)
        self.compiler.data.add('_itoa_radix', 'dd', '10')
        self.compiler.bss.add('_char', 'resb', 1)
        self.is_loaded = True

    def call(self):
        self.compiler.code.add('call', ['itoa'])
