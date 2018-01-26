from .commands import Commands
from .registers import Registers
from .config import *


class Code(list):
    stack_balance = 0

    def fix_stack_balance(self):
        if self.stack_balance != 0:
            for i in range(1, self.stack_balance):
                self.add(Commands.ADD, [Registers.ESP, 4])
                self.stack_balance -= 1

    def stack_pop(self):
        self.stack_balance -= 1
        self.add(Commands.ADD, [Registers.ESP, 4])

    def add_label(self, label_name):
        self.add(str(label_name) + ':')

        return self

    def add(self, command, args=None):
        if command == Commands.PUSH:
            self.stack_balance += 1
        elif command == Commands.POP:
            self.stack_balance -= 1

        if not isinstance(args, list):
            args = [args] if args is not None else []

        self.append(command + '\t\t' + ASM_ARGS_SEPARATOR.join(str(x) for x in args))

        return self
