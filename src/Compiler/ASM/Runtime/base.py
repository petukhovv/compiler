import os


class Base:
    path = '/asm/'

    def __init__(self, compiler):
        self.compiler = compiler

    def load(self, file, func_names):
        dir = os.path.dirname(os.path.abspath(__file__))
        f = open(dir + self.path + file, 'r')
        code = f.read()
        self.compiler.add_runtime_func(code, func_names)
