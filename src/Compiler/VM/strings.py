from Helpers.string import *

def char(commands, env, character):
    commands.add(Push, ord(character))

def string(commands, env, characters):
    for character in characters:
        char(commands, env, character)
    commands.add(Push, 0)

def strlen(commands, env, args):
    allocate_type = Environment.get_allocate_var(env, args.elements[0].name)

    args.elements[0].compile_vm(commands, env)

    String.compile_strlen(commands, env, allocate_type)

def strget(commands, env, args):
    allocate_type = Environment.get_allocate_var(env, args.elements[0].name)

    args.elements[0].compile_vm(commands, env)
    args.elements[1].compile_vm(commands, env)

    String.compile_strget(commands, env, allocate_type)

def strset(commands, env, args):
    args.elements[0].compile_vm(commands, env)
    args.elements[1].compile_vm(commands, env)
    args.elements[2].compile_vm(commands, env)
    String.compile_strset(commands, env)

def strsub(commands, env, args):
    args.elements[0].compile_vm(commands, env)
    args.elements[1].compile_vm(commands, env)
    args.elements[2].compile_vm(commands, env)
    String.compile_strsub(commands, env)
