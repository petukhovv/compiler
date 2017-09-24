# -*- coding: utf-8 -*-

from pprint import pprint

ASM_COMMANDS_SEPARATOR = '\n'
ASM_ARGS_SEPARATOR = ','

class NASMData(list):
    def add(self, label, command, data):
        self.append(label + ': ' + command + ' ' + data + '\n')

class NASMBSS(list):
    def add(self, label, command, data):
        self.append(label + ': ' + command + ' ' + data + '\n')

class NASMCode(list):
    def add(self, command, args):
        self.append(command + ' ' + ASM_ARGS_SEPARATOR.join(str(x) for x in args))

class NASMCompiler():
    def __init__(self):
        self.data = NASMData()
        self.bss = NASMBSS()
        self.code = NASMCode()

    def assemble(self):
        return (
            'SECTION .data\n' +
            ASM_COMMANDS_SEPARATOR.join(self.data) +
            'SECTION .bss\n' +
            ASM_COMMANDS_SEPARATOR.join(self.bss) +
            'SECTION .text\n' +
            'global start\n' +
            'start:\n' +
            ASM_COMMANDS_SEPARATOR.join(self.code)
        )

""" Запуск компилятора в код языка ассемблера NASM (x86) """
def compile_x86(ast):
    compiler = NASMCompiler()

    ast.compile_x86(compiler)

    return compiler.assemble()
