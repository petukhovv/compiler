# -*- coding: utf-8 -*-

from .commands import *


# Мапа соответствий: строковое представление команды VM - класс команды VM
commands_map = {
    'PUSH': Push,
    'POP': Pop,
    'NOP': Nop,
    'DUP': Dup,
    'LOAD': Load,
    'PLOAD': PLoad,
    'BLOAD': BLoad,
    'BPLOAD': BPLoad,
    'DLOAD': DLoad,
    'DBLOAD': DBLoad,
    'STORE': Store,
    'PSTORE': PStore,
    'BSTORE': BStore,
    'BPSTORE': BPStore,
    'DSTORE': DStore,
    'DBSTORE': DBStore,
    'ADD': Add,
    'MUL': Mul,
    'SUB': Sub,
    'DIV': Div,
    'MOD': Mod,
    'INVERT': Invert,
    'COMPARE': Compare,
    'LABEL': Label,
    'JUMP': Jump,
    'JZ': Jz,
    'JNZ': Jnz,
    'READ': Read,
    'WRITE': Write,
    'ENTER': Enter,
    'CALL': Call,
    'FUNCTION': Function,
    'RETURN': Return,
    'MALLOC': Malloc,
    'DMALLOC': DMalloc,
    'LOG': Log
}

# Разделитель команд VM
COMMAND_SEPARATOR = '\n'

# Разделитель аргументов команд VM
ARGS_SEPARATOR = ' '
