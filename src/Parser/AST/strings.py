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


class String(AST):
    def __init__(self, characters):
        super().__init__(CLASS, "string")

        self.characters = characters

    def interpret(self, env):
        return interpreter.string(env, self.characters)


class StrLen(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strlen")

        self.args = args
        self.children = [args]

    def interpret(self, env):
        return interpreter.str_len(env, self.args)


class StrGet(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strget")

        self.args = args
        self.children = [args]

    def interpret(self, env):
        return interpreter.str_get(env, self.args)


class StrSub(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strsub")

        self.args = args
        self.children = [args]

    def interpret(self, env):
        return interpreter.str_sub(env, self.args)


class StrDup(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strdup")

        self.args = args
        self.children = [args]

    def interpret(self, env):
        return interpreter.str_dup(env, self.args)


class StrSet(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strset")

        self.args = args
        self.children = [args]

    def interpret(self, env):
        return interpreter.str_set(env, self.args)


class StrCat(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strcat")

        self.args = args
        self.children = [args]

    def interpret(self, env):
        return interpreter.str_cat(env, self.args)


class StrCmp(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strcmp")

        self.args = args
        self.children = [args]

    def interpret(self, env):
        return interpreter.str_cmp(env, self.args)


class StrMake(AST):
    def __init__(self, args):
        super().__init__(CLASS, "strmake")

        self.args = args
        self.children = [args]

    def interpret(self, env):
        return interpreter.str_make(env, self.args)
