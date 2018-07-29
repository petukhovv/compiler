import sys

from .environment import Environment

RECURSION_LIMIT = 10000

sys.setrecursionlimit(RECURSION_LIMIT)


def interpret(ast):
    ast.interpret(Environment().create())
