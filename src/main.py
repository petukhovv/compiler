import sys
import argparse
import os

from Lexer.run import run as lex
from Parser.run import parse
from Interpreter.Helpers.run import interpret
from Compiler.VM.Helpers.run import compile_vm
from Compiler.X86.Helpers.run import compile_x86
from VM.parser import parse as vm_parse
from VM.run import run as vm_interpret

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--interpret', '-i', nargs=1, type=str, help='interpret and run')
group.add_argument('--stack_machine', '-s', nargs=1, type=str, help='compile in virtual machine code and run')
group.add_argument('--compile', '-o', nargs=1, type=str, help='compile in nasm code and then executable file')

args = parser.parse_args()


def parse_program(target_file):
    program = open(target_file).read()
    tokens = lex(program)
    parse_result = parse(tokens)
    if not parse_result:
        sys.stderr.write('Parse error!\n')
        exit()
    return parse_result.value


if args.interpret:
    target_file = args.interpret[0]
    ast = parse_program(target_file)
    interpret(ast)

if args.stack_machine:
    target_file = args.stack_machine[0]
    ast = parse_program(target_file)
    vm_program = compile_vm(ast)
    commands = vm_parse(vm_program)
    vm_interpret(commands)

if args.compile:
    target_file = args.compile[0]
    ast = parse_program(target_file)
    nasm_program = compile_x86(ast)

    filename = os.path.splitext(os.path.basename(target_file))[0]
    runtime = os.environ.get('RC_RUNTIME')
    basepath = runtime + '/' + filename

    if not os.path.exists(runtime):
        os.makedirs(runtime)

    with open(basepath + '.asm', 'w') as f:
        f.write(nasm_program)

    os.system('nasm -g -f macho ' + basepath + '.asm')
    os.system('gcc -m32 -Wl,-no_pie -o ./' + filename + ' ' + basepath + '.o')
