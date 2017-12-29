from .environment import *


def interpret(ast):
    ast.eval(Environment().create())
