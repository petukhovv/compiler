from .types import *


def token(regexp, tag, right_context='', left_context=''):
    """ Make token definition (regexp with optional left or right context) """
    return r'' + left_context + '(' + regexp + ')' + right_context + '', tag


def keyword(name):
    """ Make keyword definition (token with RESERVED type) """
    return token(name, RESERVED, right_context='\W')


token_expressions = [
    token('[ \n\t]+', None),    # Whitespaces (source code only, unused in parser)
    token('#[^\n]*', None),     # Comments (source code only, unused in parser)

    token('true|false', BOOLEAN, right_context='\W'),
    token('\"(.*?)\"', STRING),
    token('\'(.)\'', CHAR),

    # Language reserved special characters
    token('\'', None),
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
    token('!!', RESERVED),      # Same as the || (logical 'or')
    token('!', RESERVED),
    token(',', RESERVED),
    token('\[', RESERVED),
    token('\]', RESERVED),
    token('\{', RESERVED),
    token('\}', RESERVED),
    token('\.', RESERVED),

    # Language reserved keywords
    keyword('if'),
    keyword('then'),
    keyword('else'),
    keyword('elif'),
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
    keyword('fun'),
    keyword('begin'),
    keyword('return'),
    keyword('end'),
    keyword('val'),
    keyword('method'),

    token('\d+', INT),          # Integers regexp
    token('[A-Za-z]\w*', ID)    # Identifiers regexp (variable names, function names, etc)
]
