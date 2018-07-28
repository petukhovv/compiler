from Compiler.VM import strings as compile_vm
from Interpreter import strings as interpreter
from Compiler.ASM import strings as compile_asm

from .base import AST

CLASS = "strings"


class Char(AST):
    def __init__(self, character):
        super().__init__(CLASS, "char")

        self.character = character

    def interpret(self, env):
        return interpreter.char(env, self.character)

    def compile_vm(self, commands, data):
        return compile_vm.char(commands, data, self.character)


class String(AST):
    def __init__(self, characters):
        super().__init__(CLASS, "string")

        self.characters = characters

    def interpret(self, env):
        return interpreter.string(env, self.characters)

    def compile_vm(self, commands, data):
        return compile_vm.string(commands, data, self.characters)


class StrLen(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strlen")

        self.args = args
        self.children = [args]

    def interpret(self, env):
        return interpreter.str_len(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.strlen(commands, data, self.args)


class StrGet(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strget")

        self.args = args
        self.children = [args]

    def interpret(self, env):
        return interpreter.str_get(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.strget(commands, data, self.args)


class StrSub(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strsub")

        self.args = args
        self.children = [args]

    def interpret(self, env):
        return interpreter.str_sub(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.strsub(commands, data, self.args)


class StrDup(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strdup")

        self.args = args
        self.children = [args]

    def interpret(self, env):
        return interpreter.str_dup(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.strdup(commands, data, self.args)


class StrSet(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strset")

        self.args = args
        self.children = [args]

    def interpret(self, env):
        return interpreter.str_set(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.strset(commands, data, self.args)


class StrCat(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strcat")

        self.args = args
        self.children = [args]

    def interpret(self, env):
        return interpreter.str_cat(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.strcat(commands, data, self.args)


class StrCmp(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strcmp")

        self.args = args
        self.children = [args]

    def interpret(self, env):
        return interpreter.str_cmp(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.strcmp(commands, data, self.args)


class StrMake(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strmake")

        self.args = args
        self.children = [args]

    def interpret(self, env):
        return interpreter.str_make(env, self.args)

    def compile_vm(self, commands, data):
        return compile_vm.strmake(commands, data, self.args)
