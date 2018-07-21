from .base import Base


class ItoaWrite(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if ItoaWrite.is_loaded:
            return

        self.load('itoa_and_write.asm', 'itoa_and_write')
        ItoaWrite.is_loaded = True
