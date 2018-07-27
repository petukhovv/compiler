from ..Runtime.gc import GC
from ..Core.registers import Registers
from ..Core.commands import Commands


def return_function(compiler, args):
    GC(compiler).check_args(args)
    GC(compiler).check_local_vars()

    compiler.code.add(Commands.POP, Registers.EBX)
    compiler.code.add(Commands.POP, Registers.EAX)
    # Компилируем конструкцию возврата к месту вызова
    compiler.code.add(Commands.MOV, [Registers.ESP, Registers.EBP]) \
        .add(Commands.POP, Registers.EBP) \
        .add(Commands.RET, len(args) * 8)
