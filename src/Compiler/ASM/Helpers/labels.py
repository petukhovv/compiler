from ..Config.general import *


class Labels(list):
    def __init__(self):
        self.labels_counter = 0
        self.label_names_prefix = '_label_'

    def create(self):
        self.labels_counter += 1

        return self.label_names_prefix + str(self.labels_counter)

    def add(self, code):
        code_lines = code.split(ASM_COMMANDS_SEPARATOR)
        for code_line in code_lines:
            self.append(code_line)
