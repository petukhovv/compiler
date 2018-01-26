from ..Core.commands import Commands
from ..Core.registers import Registers


class TrueResult:
    label_name = '_set_true_result_'
    ret_label_name_prefix = '_ret_true_result_'
    counter = 1

    def __init__(self, compiler):
        self.compiler = compiler
        self.current_number = TrueResult.counter
        TrueResult.counter += 1

        self.add()

    def get(self):
        return self.label_name + str(self.current_number)

    def add(self):
        prolog = [
            '%s %s, 1' % (Commands.MOV, Registers.EAX),
            'jmp %s' % self.ret_label_name_prefix + str(self.current_number)
        ]
        self.compiler.labels.add(
            '%s%s:\n   %s\n   %s' % (self.label_name, str(self.current_number), prolog[0], prolog[1])
        )

        return self

    def add_return(self):
        self.compiler.code.add(self.ret_label_name_prefix + str(self.current_number) + ':', [])

