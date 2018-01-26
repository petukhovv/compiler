# -*- coding: utf-8 -*-

from .environment import Environment
from .types import *
from .commands import Commands

ASM_COMMANDS_SEPARATOR = '\n'
ASM_ARGS_SEPARATOR = ','


class Data(list):
    def add(self, label, command, data):
        self.append(label + ': ' + command + ' ' + str(data) + ASM_COMMANDS_SEPARATOR)


class CommandsHelper:
    def __init__(self, compiler):
        self.compiler = compiler

    def set_and_return_type(self, value_type):
        self.compiler.code.add(Commands.PUSH, [value_type])

        return value_type

    def clean_type(self):
        self.compiler.code.stack_pop()


class Vars:
    def __init__(self, bss, code, compiler, environment):
        self.bss = bss
        self.code = code
        self.compiler = compiler
        self.environment = environment
        self.vars = {}
        self.var_counter = 0

    def add(self, name, asm_type, bytes, type=None):
        if name in self.vars:
            return

        if name is None:
            name = self.var_counter
            self.var_counter += 1

        self.vars[name] = {
            'type': type
        }
        self.bss.add('_var_' + str(name), asm_type, bytes)
        if type:
            self.bss.add('_var_type_' + str(name), asm_type, 1)
            self.code.add(Commands.MOV, ['dword [%s]' % ('_var_type_' + str(name)), type])

        return '_var_' + str(name)

    def pop(self, name):
        self.compiler.code.add(Commands.POP, ['dword [%s]' % name])

    def get(self, name):
        env = self.environment
        if env.current_function and 'args' in env.labels[env.current_function]\
                and name in env.labels[env.current_function]['args']:
            args = env.labels[env.current_function]['args']
            arg_number = args[name]
            offset = (len(args) - arg_number - 1) * 4 + 8
            return 'dword [ebp + ' + str(offset) + ']'
        else:
            return 'dword [_var_' + str(name) + ']'

    def get_type(self, name):
        return 'dword [_var_type_' + str(name) + ']'

    def get_compile_time_type(self, name):
        return self.vars[name]['type'] if name in self.vars else Types.DYNAMIC


class BSS(list):
    def __init__(self, compiler, code, environment):
        self.vars = Vars(self, code, compiler, environment)

    def add(self, name, type, bytes):
        self.append(name + '\t\t' + type + ' ' + str(bytes) + ASM_COMMANDS_SEPARATOR)


class Code(list):
    stack_balance = 0

    def check_and_fix_stack_balance(self):
        if self.stack_balance != 0:
            for i in range(1, self.stack_balance):
                self.add(Commands.ADD, ['esp', 4])
                self.stack_balance -= 1

    def stack_pop(self):
        self.stack_balance -= 1
        self.add(Commands.ADD, ['esp', 4])

    def add(self, command, args):
        if command == Commands.PUSH:
            self.stack_balance += 1
        elif command == Commands.POP:
            self.stack_balance -= 1

        self.append(command + '\t\t' + ASM_ARGS_SEPARATOR.join(str(x) for x in args))


class Labels(list):
    def __init__(self, bss):
        self.bss = bss
        self.labels_counter = 0
        self.label_names_prefix = '_label_'

    def create(self):
        self.labels_counter += 1

        return self.label_names_prefix + str(self.labels_counter)

    def add(self, code):
        code_lines = code.split(ASM_COMMANDS_SEPARATOR)
        for code_line in code_lines:
            self.append(code_line)


class Compiler:
    def __init__(self):
        self.data = Data()
        self.environment = Environment()
        self.code = Code()
        self.bss = BSS(self, self.code, self.environment)
        self.commands = CommandsHelper(self)
        self.labels = Labels(self.bss)
        self.target_register = None

    def exit(self):
        self.code.add(Commands.PUSH, [0])
        self.code.add(Commands.MOV, ['eax', 1])
        self.code.add(Commands.SUB, ['esp', 1])
        self.code.add(Commands.INT, [0x80])

    def assemble(self):
        self.exit()

        return (
            'EXTERN _malloc' + ASM_COMMANDS_SEPARATOR +
            'SECTION .data' + ASM_COMMANDS_SEPARATOR +
            ASM_COMMANDS_SEPARATOR.join(self.data) +
            'SECTION .bss' + ASM_COMMANDS_SEPARATOR +
            ASM_COMMANDS_SEPARATOR.join(self.bss) +
            'SECTION .text' + ASM_COMMANDS_SEPARATOR +
            'global _main' + ASM_COMMANDS_SEPARATOR +
            ASM_COMMANDS_SEPARATOR.join(self.labels) + ASM_COMMANDS_SEPARATOR +
            '_main:' + ASM_COMMANDS_SEPARATOR +
            ASM_COMMANDS_SEPARATOR.join(self.code) + ASM_COMMANDS_SEPARATOR
        )


def compile_x86(ast):
    """ Запуск компилятора в код языка ассемблера NASM (x86) """
    compiler = Compiler()

    ast.compile_x86(compiler)

    return compiler.assemble()
