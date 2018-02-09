from ..Core.commands import Commands
from ..Core.registers import Registers


def run(compiler):
    gc_not_need = compiler.labels.create()

    compiler.code.add(Commands.CMP, [Registers.EAX, 0]) \
        .add(Commands.JNZ, gc_not_need)\
        .add(Commands.SUB, [Registers.EAX, 2])\
        .add(Commands.MOV, [Registers.BX, 'word [%s]' % Registers.EAX])\
        .add(Commands.SUB, [Registers.BX, 1])\
        .add(Commands.MOV, ['word [%s]' % Registers.EAX, Registers.BX])\
        .add(Commands.NOP)\
        .add_label(gc_not_need)
