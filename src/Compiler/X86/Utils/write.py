from pprint import pprint

from ..Helpers.types import *

from base import Base
from itoa import Itoa

class Write(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if self.is_loaded:
            return

        self.load('write.asm')
        self.is_loaded = True

    def call(self, value_type):
        if value_type == Types.INT or True:
            Itoa(self.compiler)
            self.compiler.code.add('call', ['_itoa'])
        else:
            pass
