from ..Utils.atoi import *
from ..Helpers.registers import Registers
from ..Helpers.commands import Commands

from .write import Write


class Read(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if Read.is_loaded:
            return

        self.load('read.asm')
        self.compiler.vars.add_in_bss('_read_buffer', 'resb', 255)
        self.compiler.vars.add_in_bss('_read_buffer_done', 'resb', 4)
        self.compiler.vars.add_in_bss('_read_buffer_all', 'resb', 4)
        self.compiler.vars.add_in_data('_read_buffer_size', 'dd', '255')
        Read.is_loaded = True

        Write(compiler)

    def call(self):
        self.compiler.code.add(Commands.CALL, ['_read'])
        self.compiler.code.add(Commands.MOV, ['[_read_buffer_all]', Registers.EAX])

        Atoi(self.compiler)

        self.compiler.code.add(Commands.MOV, [Registers.EAX, 62])
        self.compiler.code.add(Commands.CALL, ['_write'])
        self.compiler.code.add(Commands.MOV, [Registers.EAX, 32])
        self.compiler.code.add(Commands.CALL, ['_write'])

        self.compiler.code.add(Commands.MOV, [Registers.ESI, '_read_buffer'])
        self.compiler.code.add(Commands.MOV, [Registers.EAX, 0])
        self.compiler.code.add(Commands.CALL, ['_atoi'])
        self.compiler.code.add(Commands.PUSH, [Registers.EAX])
