import sys
import re


def lex(code, token_expressions):
    """
    Lexer breaks the code into tokens by regex (token expressions).
    Order of tokens in token expressions is important.
    Lexer applies only the first match found.
    1) the first must be unused (in parser) constructions: whitespaces and comments
    2) then - strings, chars and boolean definition
    3) then - language expressions: +, :=, and, if, while, etc;
    4) then - identifiers (e. g. variable names) and numbers
    """
    pos = 0
    tokens = []
    while pos < len(code):
        match = None
        for token_expression in token_expressions:
            pattern, tag = token_expression
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                text = match.group(len(match.groups()))
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        if not match:
            sys.stderr.write('Illegal character: %s\n' % code[pos])
            sys.exit(1)
        else:
            pos = match.end(1)
    return tokens
