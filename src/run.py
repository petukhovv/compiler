import sys
sys.path.append('src/..')

from os.path import isfile

from Lexer.tokenizer import tokenize
from Parser.run import parse
from pprint import pprint

help_commands = '-i - interpret, -s - compile in virtual machine code, -o - compile in executable file'

if len(sys.argv) <= 1:
    sys.stderr.write('Mode not specified (' + help_commands + ').\n')
    exit()

mode = sys.argv[1]

if mode not in ['-i', '-s', '-o']:
    sys.stderr.write('Mode is incorrect (' + help_commands + ').\n')
    exit()

if len(sys.argv) <= 2:
    sys.stderr.write('Source code file not specified.\n')
    exit()

target_file = sys.argv[2]

if not isfile(target_file):
    sys.stderr.write('Source code file not found (incorrect path: "' + target_file + '").\n')
    exit()

def parse_program(program):
    tokens = tokenize(program)
    parse_result = parse(tokens)
    if not parse_result:
        sys.stderr.write('Parse error!\n')
        exit()
    return parse_result.value

program = open(target_file).read()

if mode == '-i':
    ast = parse_program(program)
    env = {
        'v': {},    # variables environment
        'f': {},    # functions environment
        'p': None   # parent environment
    }
    ast.eval(env)
