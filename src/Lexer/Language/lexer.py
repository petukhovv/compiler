from src.Lexer.lexer import lexer

"""
RESERVED is language expressions.
INT is whole numbers (integers).
ID is identifiers (e. g. variable names).
"""
RESERVED = 'RESERVED'
INT = 'INT'
ID = 'ID'

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

    (r'[0-9]+', INT),

    (r'[A-Za-z][A-Za-z0-9_]*', ID)
]

"""
Function-wrapper to run the Lexer (with the token expressions listed here).
"""
def tokenize(code):
    return lexer(code, token_expressions)
