from .commands import Commands
from .registers import Registers
from .config import *

from ..Runtime.write import Write


class Code(list):
    stack_align_points = []
    stack = {
        'size': 4,
        'balance': 0
    }

    def __init__(self, compiler):
        self.compiler = compiler

    def fix_stack_balance(self):
        if self.stack['balance'] != 0:
            for i in range(1, self.stack['balance']):
                self.add(Commands.ADD, [Registers.ESP, 4])
                self.stack['balance'] -= 1

    def add_stack_align_point(self, multiplicity):
        self.stack_align_points.append({
            'place': len(self),
            'multiplicity': multiplicity
        })

    def stack_align(self, multiplicity, offset=0):
        self.add(Commands.MOV, [Registers.EAX, Registers.EBP])
        self.add(Commands.SUB, [Registers.EAX, Registers.ESP])

        self.add(Commands.XOR, [Registers.EDX, Registers.EDX])
        self.add(Commands.MOV, [Registers.EBX, multiplicity])
        self.add(Commands.DIV, [Registers.EBX])
        self.add(Commands.MOV, [Registers.EAX, multiplicity])
        self.add(Commands.SUB, [Registers.EAX, Registers.EDX])
        if offset != 0:
            self.add(Commands.ADD, [Registers.EAX, offset])
        self.add(Commands.SUB, [Registers.ESP, Registers.EAX])
        self.add(Commands.PUSH, Registers.EAX)

    def restore_stack_align(self):
        self.add(Commands.POP, Registers.EBX)
        self.add(Commands.ADD, [Registers.ESP, Registers.EBX])

    def stack_pop(self):
        self.stack['balance'] -= 1
        self.add(Commands.ADD, [Registers.ESP, 4])

    def allocate_stack_memory(self, memory_size, place):
        self.add(Commands.SUB, [Registers.ESP, memory_size], index=place)

    def add_label(self, label_name, place=None):
        self.add(str(label_name) + ':', index=place)

        return self

    def stack_size_write(self, stack_obj, command, args):
        if command == Commands.PUSH:
            stack_obj['balance'] += 1
        elif command == Commands.POP:
            stack_obj['balance'] -= 1

    def add(self, command, args=None, index=None):
        self.stack_size_write(self.stack, command, args)

        if not isinstance(args, list):
            args = [args] if args is not None else []

        if index is not None:
            self.insert(index, (command, args))
        else:
            self.append((command, args))

        return self

    def log(self):
        self.add(Commands.CALL, 'itoa')
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
