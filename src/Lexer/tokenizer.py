from src.Lexer.lexer import lex
from src.consts import *

"""
Wrapper for tokenization.
Make one parentheses group with optional right context.
"""
def token(regexp, tag, right_context=''):
    return r'(' + regexp + ')' + right_context + '', tag

"""
Wrapper for tokenization language keywords.
Keyword is token with non-alphanumeric right context.
"""
def keyword(keyword):
    return token(keyword, RESERVED, right_context='\W')

token_expressions = [
    token('[ \n\t]+', None),
    token('#[^\n]*', None),

    token('\:=', RESERVED),
    token('\(', RESERVED),
    token('\)', RESERVED),
    token(';', RESERVED),
    token('\+', RESERVED),
    token('-', RESERVED),
    token('\*', RESERVED),
    token('/', RESERVED),
    token('%', RESERVED),
    token('<=', RESERVED),
    token('<', RESERVED),
    token('>=', RESERVED),
    token('>', RESERVED),
    token('!=', RESERVED),
    token('==', RESERVED),
    token('\&\&', RESERVED),
    token('\|\|', RESERVED),
    token('!', RESERVED),
    token(',', RESERVED),

    keyword('if'),
    keyword('then'),
    keyword('else'),
    keyword('fi'),
    keyword('while'),
    keyword('do'),
    keyword('od'),
    keyword('repeat'),
    keyword('until'),
    keyword('for'),
    keyword('read'),
    keyword('write'),
    keyword('skip'),

    token('\d+', INT),
    token('[A-Za-z]\w*', ID)
]

"""
Function-wrapper to run the Lexer (with the token expressions listed here).
"""
def tokenize(code):
    return lex(code, token_expressions)
