from src.VM.commands import *
from src.VM.Helpers.assembler import *
from Helpers.string import *

def char(commands, env, character):
    commands.append(assemble(Push, ord(character)))

def string(commands, env, characters):
    commands.append(assemble(Push, 0))
    for character in characters:
        char(commands, env, character)

def strlen(commands, env, args):
    args.elements[0].compile_vm(commands, env)
    String.compile_strlen(commands, env)

def strget(commands, env, args):
    args.elements[0].compile_vm(commands, env)
    args.elements[1].compile_vm(commands, env)
    String.compile_strget(commands, env)
