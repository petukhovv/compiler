from .rules import token_expressions
from .lex import lex


def run(code):
    """ Wrapper to run the Lexer (with the token expressions listed here). """
    return lex(code, token_expressions)
