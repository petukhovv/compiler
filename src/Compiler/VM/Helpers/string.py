from src.VM.Helpers.assembler import *
from environment import *

class String:
    @staticmethod
    def compile_strlen(commands, env):
        start_while_label = Environment.create_label(env)
        end_while_label = Environment.create_label(env)
        counter_var = Environment.create_var(env)

        commands.append(assemble(Push, 0))
        commands.append(assemble(Store, counter_var))
        commands.append(assemble(Label, start_while_label))
        commands.append(assemble(Dup))
        commands.append(assemble(Jz, end_while_label))
        commands.append(assemble(Pop))
        commands.append(assemble(Load, counter_var))
        commands.append(assemble(Push, 1))
        commands.append(assemble(Add))
        commands.append(assemble(Store, counter_var))
        commands.append(assemble(Jump, start_while_label))
        commands.append(assemble(Label, end_while_label))
        commands.append(assemble(Pop))
        commands.append(assemble(Load, counter_var))

    @staticmethod
    def compile_get(commands, env, var_number):
        start_while_label = Environment.create_label(env)
        end_while_label = Environment.create_label(env)
        counter_var = Environment.create_var(env)
        commands.append(assemble(Push, 0))
        commands.append(assemble(Load, var_number))
        commands.append(assemble(BLoad, 0))
        commands.append(assemble(Push, 0))
        commands.append(assemble(Store, counter_var))
        commands.append(assemble(Label, start_while_label))
        commands.append(assemble(Dup))
        commands.append(assemble(Jz, end_while_label))
        commands.append(assemble(Load, var_number))
        commands.append(assemble(Load, counter_var))
        commands.append(assemble(Push, 1))
        commands.append(assemble(Add))
        commands.append(assemble(Store, counter_var))
        commands.append(assemble(Load, counter_var))
        commands.append(assemble(Add))
        commands.append(assemble(BLoad, 0))
        commands.append(assemble(Jump, start_while_label))
        commands.append(assemble(Label, end_while_label))
        commands.append(assemble(Pop))

    @staticmethod
    def compile_set(commands, env, characters):
        pointer_start_string = 0
        for char in characters:
            var_number = Environment.create_var(env)
            if pointer_start_string == 0:
                pointer_start_string = var_number
            commands.append(assemble(Store, var_number))
        commands.append(assemble(Store, Environment.create_var(env)))
        commands.append(assemble(Push, pointer_start_string))
