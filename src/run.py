import sys
sys.path.append(len(sys.argv) == 4 and sys.argv[3] or 'src/..')

from os import path, remove, system

from Lexer.tokenizer import tokenize
from Parser.run import parse
from Interpreter.Helpers.run import interpret
from Compiler.VM.Helpers.run import compile_vm
from Compiler.X86.Helpers.run import compile_x86
from src.VM.parser import parse as vm_parse
from VM.run import run as vm_interpret

help_commands = '-i - run, -s - compile in virtual machine code, -o - compile in executable file'

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

if not path.isfile(target_file):
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
ast = parse_program(program)

if mode == '-i':
    interpret(ast)

if mode == '-s':
    vm_program = compile_vm(ast)
    # f = open('src/test_vm2_out', 'w')
    # f.write(vm_program)
    commands = vm_parse(vm_program)
    vm_interpret(commands)

if mode == '-o':
    format = 'macho'
    nasm_program = compile_x86(ast)
    f = open('./program.asm', 'w')
    f.write(nasm_program)
    f.close()
    system('nasm -f ' + format + ' ./program.asm')
    system('ld -o ./program ./program.o')
    remove('./program.o')
    remove('./program.asm')
    system('./program')
    remove('./program')
