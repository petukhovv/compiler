
from ...Core.registers import Registers
from ...Core.commands import Commands
from ...Runtime.gc import GC

from ...Deep.functions import return_function


def return_statement(compiler, node):
    """ Компиляция выражения возврата к месту вызова """
    args = compiler.environment.get_args()
    return_type = node.expr.compile_asm(compiler)
    compiler.environment.set_return_type(return_type)

    compiler.code.add(Commands.MOV, [Registers.EAX, 'dword [%s + 4]' % Registers.ESP])
    compiler.code.add(Commands.MOV, [Registers.EBX, 'dword [%s]' % Registers.ESP])
    GC(compiler).increment()

    return_function(compiler, args)