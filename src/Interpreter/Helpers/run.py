import sys

from .environment import *

RECURSION_LIMIT = 10000

sys.setrecursionlimit(RECURSION_LIMIT)


def interpret(ast):
    ast.interpret(Environment().create())
