import sys
import re


def lexer(code, token_expressions):
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
