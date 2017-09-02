from Helpers.string import *

AST = sys.modules['src.Parser.AST.strings']

def char(commands, env, character):
    commands.add(Push, ord(character))

def string(commands, env, characters):
    commands.add(Push, 0)
    for character in characters:
        char(commands, env, character)
    commands.add(Push, len(characters))

def strlen(commands, env, args):
    args.elements[0].compile_vm(commands, env)
    if isinstance(args.elements[0], AST.String):
        StringCompiler._store(commands, env)

    StringCompiler.strlen(commands, env)

def strget(commands, env, args):
    args.elements[1].compile_vm(commands, env)
    args.elements[0].compile_vm(commands, env)
    if isinstance(args.elements[0], AST.String):
        StringCompiler._store(commands, env)

    StringCompiler.strget(commands, env)

def strset(commands, env, args):
    args.elements[2].compile_vm(commands, env)
    args.elements[1].compile_vm(commands, env)
    args.elements[0].compile_vm(commands, env)

    StringCompiler.strset(commands, env)

def strsub(commands, env, args):
    args.elements[1].compile_vm(commands, env)
    args.elements[0].compile_vm(commands, env)
    if isinstance(args.elements[0], AST.String):
        StringCompiler._store(commands, env)
    args.elements[2].compile_vm(commands, env)

    StringCompiler.strsub(commands, env)

def strdup(commands, env, args):
    args.elements[0].compile_vm(commands, env)
    if isinstance(args.elements[0], AST.String):
        StringCompiler._store(commands, env)

    StringCompiler.strdup(commands, env)

def strcat(commands, env, args):
    args.elements[0].compile_vm(commands, env)
    StringCompiler.strcat(commands, env)
    args.elements[1].compile_vm(commands, env)
    if isinstance(args.elements[1], AST.String):
        StringCompiler._store(commands, env)

    StringCompiler.strcat_join(commands, env)
