from .base import Base


class Itoa(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if Itoa.is_loaded:
            return

        self.load('itoa.asm')
        self.compiler.vars.add_in_data('_itoa_radix', 'dd', '10')
        self.compiler.vars.add_in_bss('_char', 'resb', 4)
        Itoa.is_loaded = True
