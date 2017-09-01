from src.Compiler.VM import strings as compile_vm
from src.Interpreter import strings as interpreter

class Char:
    def __init__(self, character):
        self.character = character

    def eval(self, env):
        return interpreter.char(env, self.character)

    def compile_vm(self, commands, env):
        return compile_vm.char(commands, env, self.character)

class String:
    def __init__(self, characters):
        self.characters = characters

    def eval(self, env):
        return interpreter.string(env, self.characters)

    def compile_vm(self, commands, env):
        return compile_vm.string(commands, env, self.characters)

class StrLen:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.str_len(env, self.args)

    def compile_vm(self, commands, env):
        return compile_vm.strlen(commands, env, self.args)

class StrGet:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.str_get(env, self.args)

    def compile_vm(self, commands, env):
        return compile_vm.strget(commands, env, self.args)

class StrSub:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.str_sub(env, self.args)

    def compile_vm(self, commands, env):
        return compile_vm.strsub(commands, env, self.args)

class StrDup:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.str_dup(env, self.args)

class StrSet:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.str_set(env, self.args)

    def compile_vm(self, commands, env):
        return compile_vm.strset(commands, env, self.args)

class StrCat:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.str_cat(env, self.args)

class StrCmp:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.str_cmp(env, self.args)

class StrMake:
    def __init__(self, args):
        self.args = args

    def eval(self, env):
        return interpreter.str_make(env, self.args)
