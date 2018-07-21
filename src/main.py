import argparse
import os
import sys

from Compiler.ASM.Core.run import compile_asm
from Compiler.VM.Helpers.run import compile_vm
from Interpreter.Helpers.run import interpret
from Lexer.run import run as lex
from Parser.run import parse
from Parser.Helpers.ast_printer import ast_print
from VM.parser import parse as vm_parse
from VM.run import run as vm_interpret

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--interpret', '-i', nargs=1, type=str, help='interpret and run')
group.add_argument('--stack_machine', '-s', nargs=1, type=str, help='compile in virtual machine code and run')
group.add_argument('--compile', '-o', nargs=1, type=str, help='compile in nasm code and then executable file')
parser.add_argument('--ast_print', action='store_true', help='whether to output the AST')

args = parser.parse_args()
ast_print_arg = args.ast_print


def parse_program(target_file):
    program = open(target_file).read()
    tokens = lex(program)
    parse_result = parse(tokens)
    if not parse_result:
        print('Parse error!')
        exit()
       
    ast = parse_result.value

    if ast_print_arg:
        print(ast)

    return ast


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

    program, runtime = compile_asm(ast)

    filename = os.path.splitext(os.path.basename(target_file))[0]
    runtime_folder = os.environ.get('RC_RUNTIME')
    program_path = '%s/%s' % (runtime_folder, filename)
    runtime_path = '%s/runtime' % runtime_folder

    if not os.path.exists(runtime_folder):
        os.makedirs(runtime_folder)

    with open('%s.asm' % runtime_path, 'w') as f:
        f.write(runtime)

    with open('%s.asm' % program_path, 'w') as f:
        f.write(program)

    os.system('nasm -g -f macho -l %s.lst %s.asm' % (runtime_path, runtime_path))
    os.system('nasm -g -f macho -l %s.lst %s.asm' % (program_path, program_path))
    os.system('gcc -m32 -Wl,-no_pie -o ./%s %s.o %s.o' % (filename, runtime_path, program_path))
