import sys
sys.path.append(len(sys.argv) == 4 and sys.argv[3] or 'src/..')

from pprint import pprint

from os.path import isfile

from Lexer.tokenizer import tokenize
from Parser.run import parse
from Interpreter.Helpers.run import interpret, compile_vm
from src.VM.Helpers.parser import parse as vm_parse
from VM.run import interpret as vm_interpret

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
    interpret(ast)

if mode == '-s':
    ast = parse_program(program)
    vm_program = compile_vm(ast)
    f = open('src/test_vm2_out', 'w')
    f.write(vm_program)
    commands = vm_parse(vm_program)
    vm_interpret(commands)
