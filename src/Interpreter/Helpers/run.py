from .environment import *


def interpret(ast):
    ast.interpret(Environment().create())
