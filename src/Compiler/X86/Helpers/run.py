# -*- coding: utf-8 -*-

VM_COMMANDS_SEPARATOR = '\n'

""" Запуск компилятора в код языка ассемблера NASM (x86) """
def compile_x86(ast):
    return 'global start\n' \
           'section .text\n' \
           'start:\n' \
           'push    dword msg.len\n' \
           'push    dword msg\n' \
           'push    dword 1\n' \
           'mov     eax, 4\n' \
           'sub     esp, 4\n' \
           'int     0x80\n' \
           'add     esp, 16\n' \
           'push    dword 0\n' \
           'mov     eax, 1\n' \
           'sub     esp, 12\n' \
           'int     0x80\n' \
           'section .data\n' \
           'msg:    db      "Hello, world!", 10\n' \
           '.len:   equ     $ - msg\n'

    commands = Commands()
    ast.compile_vm(commands, Environment())

    return VM_COMMANDS_SEPARATOR.join(commands)
