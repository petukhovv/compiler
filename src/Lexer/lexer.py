import sys
import re

"""
Lexer. It breaks the code into tokens by token expressions (regexps).
Order of tokens in token expressions is important!
Lexer applies only the first match found (the first must be language expressions: +, :=, and, if, while, etc;
then - identifiers (e. g. variable names) and numbers).
"""
def lex(code, token_expressions):
    pos = 0
    tokens = []
    while pos < len(code):
        match = None
        for token_expression in token_expressions:
            pattern, tag = token_expression
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                text = match.group(0)
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        if not match:
            sys.stderr.write('Illegal character: %s\n' % code[pos])
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens
