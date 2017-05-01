from src.Lexer.lexer import lex
from src.consts import *

"""
'None' - whitespace characters. It's ignored when parsing.
'RESERVED' - language expressions.
'INT' - whole numbers (integers).
'ID' - identifiers.
"""
token_expressions = [
    (r'[ \n\t]+', None),
    (r'#[^\n]*', None),

    (r'\:=', RESERVED),
    (r'\(', RESERVED),
    (r'\)', RESERVED),
    (r';', RESERVED),
    (r'\+', RESERVED),
    (r'-', RESERVED),
    (r'\*', RESERVED),
    (r'/', RESERVED),
    (r'<=', RESERVED),
    (r'<', RESERVED),
    (r'>=', RESERVED),
    (r'>', RESERVED),
    (r'!=', RESERVED),
    (r'=', RESERVED),
    (r'and', RESERVED),
    (r'or', RESERVED),
    (r'not', RESERVED),
    (r'if', RESERVED),
    (r'then', RESERVED),
    (r'else', RESERVED),
    (r'while', RESERVED),
    (r'do', RESERVED),
    (r'end', RESERVED),
    (r'read', RESERVED),
    (r'write', RESERVED),

    (r'[0-9]+', INT),

    (r'[A-Za-z][A-Za-z0-9_]*', ID)
]

"""
Function-wrapper to run the Lexer (with the token expressions listed here).
"""
def tokenize(code):
    return lex(code, token_expressions)
