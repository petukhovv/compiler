from .base import Base


class Itoa(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if Itoa.is_loaded:
            return

        self.load('itoa.asm')
        self.compiler.vars.add_in_bss('write_buffer', 'resb', 4)
        Itoa.is_loaded = True
