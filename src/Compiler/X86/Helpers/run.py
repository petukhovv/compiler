# -*- coding: utf-8 -*-

from pprint import pprint

ASM_COMMANDS_SEPARATOR = '\n'
ASM_ARGS_SEPARATOR = ','

class NASMData(list):
    def add(self, label, command, data):
        self.append(label + ': ' + command + ' ' + data + '\n')

class NASMBSS(list):
    def add(self, name, type, bytes):
        self.append(name + ' ' + type + ' ' + str(bytes) + '\n')

class NASMCode(list):
    def add(self, command, args):
        self.append(command + ' ' + ASM_ARGS_SEPARATOR.join(str(x) for x in args))

class NASMLabels(list):
    def add(self, code):
        code_lines = code.split('\n')
        for code_line in code_lines:
            self.append(code_line)

class NASMCompiler():
    def __init__(self):
        self.data = NASMData()
        self.bss = NASMBSS()
        self.code = NASMCode()
        self.labels = NASMLabels()
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
    compiler = NASMCompiler()

    ast.compile_x86(compiler)

    return compiler.assemble()
