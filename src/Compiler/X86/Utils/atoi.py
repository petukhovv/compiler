from pprint import pprint
import os

from .base import Base

class Atoi(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if self.is_loaded:
            return

        self.load('atoi.asm')
        self.is_loaded = True
