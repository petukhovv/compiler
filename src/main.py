import sys
import argparse
from os import remove, system

from Lexer.tokenizer import tokenize
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
group.add_argument('--compile', '-o', nargs=1, type=str, help='compile in executable file and run')

args = parser.parse_args()


def parse_program(target_file):
    program = open(target_file).read()
    tokens = tokenize(program)
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
    # f = open('src/test_vm2_out', 'w')
    # f.write(vm_program)
    commands = vm_parse(vm_program)
    vm_interpret(commands)

if args.compile:
    target_file = args.compile[0]
    ast = parse_program(target_file)
    # test_name = path.splitext(path.basename(target_file))[0]
    # nasm_program = compile_x86(ast)
    # f = open(current_dir + '/../runtime/' + test_name + '.asm', 'w')
    # f.write(nasm_program)
    # f.close()

    nasm_program = compile_x86(ast)
    f = open('./program.asm', 'w')
    f.write(nasm_program)
    f.close()
    system('nasm -f macho ./program.asm -l ./program.lst')
    system('ld -o ./program ./program.o')
    # remove('./program.o')
    # remove('./program.asm')
    system('./program')
    remove('./program')

    # system('nasm -f macho ' + current_dir + '/../runtime/' + test_name + '.asm -l ' + current_dir + '/../runtime/' + test_name + '.lst && ' +
    #        'ld -o ' + test_name + ' ' + current_dir + '/../runtime/' + test_name + '.o && ' +
    #        'rm ' + current_dir + '/../runtime/' + test_name + '.asm'
    #        )

    # p = sub.Popen([current_dir + '/program'], stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE)
    # output, errors = p.communicate()
