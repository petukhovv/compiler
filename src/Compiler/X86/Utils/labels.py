# -*- coding: utf-8 -*-

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
        self.compiler.labels.add(self.label_name + str(self.current_number) + ':\n'
                                 '   mov eax, 1\n'
                                 '   jmp ' + self.ret_label_name_prefix + str(self.current_number))

        return self

    def add_return(self):
        self.compiler.code.add(self.ret_label_name_prefix + str(self.current_number), [])

