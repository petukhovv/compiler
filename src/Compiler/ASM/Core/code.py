from .commands import Commands
from .registers import Registers
from .config import *

from ..Runtime.write import Write


class Code(list):
    def __init__(self, compiler):
        self.compiler = compiler

    def stack_pop(self):
        self.add(Commands.ADD, [Registers.ESP, 4])

    def allocate_stack_memory(self, memory_size, place):
        self.add(Commands.SUB, [Registers.ESP, memory_size], index=place)

    def add_label(self, label_name, place=None):
        self.add(str(label_name) + ':', index=place)

        return self

    def add(self, command, args=None, index=None):
        if not isinstance(args, list):
            args = [args] if args is not None else []

        if index is not None:
            self.insert(index, (command, args))
        else:
            self.append((command, args))

        return self

    def log(self):
        self.add(Commands.CALL, 'itoa_and_write')
        self.add(Commands.MOV, [Registers.EAX, 10])
        self.add(Commands.CALL, 'write')

    def get_current_place(self):
        return len(self)

    def assemble(self):
        code = []

        for command_line in self:
            (command, args) = command_line
            code.append(command + '\t\t' + ASM_ARGS_SEPARATOR.join(str(x) for x in args))

        return code
