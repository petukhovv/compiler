from Compiler.VM import strings as compile_vm
from Interpreter import strings as interpreter
from Compiler.X86 import strings as compile_x86

from .base import *


class Char(Stackable):
    def __init__(self, character):
        self.character = character

    def eval(self, env):
        return interpreter.char(env, self.character)

    def compile_vm(self, commands, data):
        return compile_vm.char(commands, data, self.character)

    def compile_x86(self, compiler):
        return compile_x86.char(compiler, self.character)


class String(Heapable):
    def __init__(self, characters):
        self.characters = characters

    def eval(self, env):
        return interpreter.string(env, self.characters)

    def compile_vm(self, commands, data):
        return compile_vm.string(commands, data, self.characters)

    def compile_x86(self, compiler):
        return compile_x86.string(compiler, self.characters)


class StrLen(Stackable):
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.str_len(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.strlen(commands, data, self.args)

    def compile_x86(self, compiler):
        return compile_x86.strlen(compiler, self.args)


class StrGet(Stackable):
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.str_get(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.strget(commands, data, self.args)

    def compile_x86(self, compiler):
        return compile_x86.strget(compiler, self.args)


class StrSub(Heapable):
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.str_sub(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.strsub(commands, data, self.args)


class StrDup(Heapable):
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.str_dup(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.strdup(commands, data, self.args)


class StrSet:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.str_set(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.strset(commands, data, self.args)

    def compile_x86(self, compiler):
        return compile_x86.strset(compiler, self.args)


class StrCat(Heapable):
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.str_cat(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.strcat(commands, data, self.args)


class StrCmp:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.str_cmp(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.strcmp(commands, data, self.args)


class StrMake:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.str_make(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.strmake(commands, data, self.args)
