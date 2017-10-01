# -*- coding: utf-8 -*-

from pprint import pprint

ASM_COMMANDS_SEPARATOR = '\n'
ASM_ARGS_SEPARATOR = ','

class Data(list):
    def add(self, label, command, data):
        self.append(label + ': ' + command + ' ' + data + '\n')

class Vars:
    def __init__(self, bss):
        self.bss = bss
        self.vars = {}

    def add(self, name, type, bytes):
        if name in self.vars:
            return

        self.vars[name] = type
        self.bss.add('_var_' + name, type, bytes)

    def get(self, name):
        return 'dword [_var_' + name + ']'

class BSS(list):
    def __init__(self):
        self.vars = Vars(self)

    def add(self, name, type, bytes):
        self.append(name + ' ' + type + ' ' + str(bytes) + '\n')

class Code(list):
    def add(self, command, args):
        self.append(command + ' ' + ASM_ARGS_SEPARATOR.join(str(x) for x in args))

class Labels(list):
    def __init__(self, bss):
        self.bss = bss
        self.labels_counter = 0
        self.label_names_prefix = '_label_'

    def create(self):
        self.labels_counter += 1

        return self.label_names_prefix + str(self.labels_counter)

    def add(self, code):
        code_lines = code.split('\n')
        for code_line in code_lines:
            self.append(code_line)

class Compiler():
    def __init__(self):
        self.data = Data()
        self.bss = BSS()
        self.code = Code()
        self.labels = Labels(self.bss)
        self.target_register = None

    def exit(self):
        self.code.add('push', [0])
        self.code.add('mov', ['eax', 1])
        self.code.add('sub', ['esp', 12])
        self.code.add('int', ['0x80'])

    def assemble(self):
        self.exit()

        return (
            'SECTION .data\n' +
            ASM_COMMANDS_SEPARATOR.join(self.data) +
            'SECTION .bss\n' +
            ASM_COMMANDS_SEPARATOR.join(self.bss) +
            'SECTION .text\n' +
            'global start\n' +
            ASM_COMMANDS_SEPARATOR.join(self.labels) + '\n'
            'start:\n' +
            ASM_COMMANDS_SEPARATOR.join(self.code) + '\n'
        )

""" Запуск компилятора в код языка ассемблера NASM (x86) """
def compile_x86(ast):
    compiler = Compiler()

    ast.compile_x86(compiler)

    return compiler.assemble()
