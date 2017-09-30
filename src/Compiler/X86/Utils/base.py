import os

class Base:
    path = '/asm/'

    def __init__(self, compiler):
        self.compiler = compiler

    def load(self, file):
        dir = os.path.dirname(os.path.abspath(__file__))
        f = open(dir + self.path + file, 'r')
        itoa_code = f.read()
        self.compiler.labels.add(itoa_code)
