from ..Core.commands import Commands
from ..Core.registers import Registers


def run(compiler):
    gc_not_need = compiler.labels.create()
    gc_free = compiler.labels.create()

    compiler.code.add(Commands.CMP, [Registers.EAX, 0]) \
        .add(Commands.JLE, gc_not_need)

    compiler.code.add(Commands.SUB, [Registers.EAX, 2])\
        .add(Commands.MOV, [Registers.BX, 'word [%s]' % Registers.EAX])\
        .add(Commands.SUB, [Registers.BX, 1])\
        .add(Commands.MOV, ['word [%s]' % Registers.EAX, Registers.BX]) \
        .add(Commands.CMP, [Registers.BX, 0]) \
        .add(Commands.JZ, gc_free) \
        .add(Commands.JMP, gc_not_need) \
        .add_label(gc_free)

    compiler.code.add(Commands.MOV, [Registers.ECX, Registers.EAX])
    compiler.code.stack_align(16, 12)
    compiler.code.add(Commands.PUSH, Registers.ECX)
    compiler.code.add(Commands.CALL, ['_free'])
    compiler.code.add(Commands.ADD, [Registers.ESP, 4])
    compiler.code.restore_stack_align()

    compiler.code.add(Commands.NOP)\
        .add_label(gc_not_need)
