from Helpers.string import *

def char(commands, env, character):
    commands.add(Push, ord(character))

def string(commands, env, characters):
    commands.add(Push, 0)
    for character in characters:
        char(commands, env, character)
    commands.add(Push, len(characters))

def strlen(commands, env, args):
    args.elements[0].compile_vm(commands, env)
    String.strlen(commands, env)

def strget(commands, env, args):
    args.elements[0].compile_vm(commands, env)
    args.elements[1].compile_vm(commands, env)

    String.strget(commands, env)

def strset(commands, env, args):
    args.elements[0].compile_vm(commands, env)
    args.elements[1].compile_vm(commands, env)
    args.elements[2].compile_vm(commands, env)
    String.strset(commands, env)

def strsub(commands, env, args):
    args.elements[0].compile_vm(commands, env)
    args.elements[1].compile_vm(commands, env)
    args.elements[2].compile_vm(commands, env)
    String.strsub(commands, env)

def strdup(commands, env, args):
    args.elements[0].compile_vm(commands, env)
    String.strdup(commands, env)
