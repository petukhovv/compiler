from .commands import Commands
from .registers import Registers
from .types import Types

from ..Config.general import *


class Vars:
    def __init__(self, compiler, code, environment):
        self.code = code
        self.compiler = compiler
        self.environment = environment
        self.vars = {}
        self.var_counter = 0
        self.bss = []
        self.data = []

    def add_in_data(self, label, command, data):
        self.data.append(label + ': ' + command + ' ' + str(data) + ASM_COMMANDS_SEPARATOR)

    def add_in_bss(self, name, type, bytes):
        self.bss.append(name + '\t\t' + type + ' ' + str(bytes) + ASM_COMMANDS_SEPARATOR)

    def add(self, name, asm_type, bytes, type=None):
        if name in self.vars:
            return

        if name is None:
            name = self.var_counter
            self.var_counter += 1

        self.vars[name] = {
            'type': type
        }
        self.add_in_bss('_var_%s' % str(name), asm_type, bytes)
        if type:
            self.add_in_bss('_var_type_%s' % str(name), asm_type, 1)
            self.code.add(Commands.MOV, ['dword [%s]' % ('_var_type_%s' % str(name)), type])

        return '_var_%s' % str(name)

    def pop(self, name):
        self.compiler.code.add(Commands.POP, ['dword [%s]' % name])

    def get(self, name):
        env = self.environment
        if env.current_function and 'args' in env.labels[env.current_function]\
                and name in env.labels[env.current_function]['args']:
            args = env.labels[env.current_function]['args']
            arg_number = args[name]
            offset = (len(args) - arg_number - 1) * 4 + 8
            return 'dword [%s + %d]' % (Registers.EBP, offset)
        else:
            return 'dword [_var_%s]' % str(name)

    def get_type(self, name):
        return 'dword [_var_type_%s]' % str(name)

    def get_compile_time_type(self, name):
        return self.vars[name]['type'] if name in self.vars else Types.DYNAMIC
