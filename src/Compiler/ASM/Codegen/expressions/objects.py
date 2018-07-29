from ...Core.types import Types
from ...Core.commands import Commands
from ...Core.registers import Registers

from copy import copy
from .call import call_statement as compile_call_statement


def object_val(compiler, node):
    if node.object_name == 'this':
        obj_var = compiler.environment.object_list[-1][0]
    else:
        if compiler.environment.current is not None:
            obj_var = compiler.environment.get_object_name(compiler.environment.get_parent_local_var(node.object_name, as_object=False))
        else:
            obj_var = compiler.environment.get_object_name(compiler.environment.get_local_var(node.object_name))

    if node.context == 'assign':
        if node.object_name == 'this':
            prop_var = compiler.environment.get_parent_local_var("var_%s_%s" % (obj_var, node.prop_name))
            compiler.code.add(Commands.MOV, [Registers.EBX, "dword [%s]" % compiler.environment.object_list[-1][1]])
            compiler.code.add(Commands.SUB, [Registers.EBX, prop_var['offset']])
            compiler.code.add(Commands.POP, 'dword [%s]' % Registers.EBX)
        else:
            if compiler.environment.current is not None:
                prop_var = compiler.environment.get_parent_local_var("var_%s_%s" % (obj_var, node.prop_name))

                if prop_var is None:
                    prop_var = compiler.environment.add_parent_local_var(Types.INT, node.prop_name, object_namespace=obj_var)

                compiler.code.add(Commands.MOV, [Registers.EBX, "dword [%s]" % compiler.environment.object_list[-1][1]])
                compiler.code.add(Commands.SUB, [Registers.EBX, prop_var['offset']])
                compiler.code.add(Commands.POP, ['dword [%s]' % Registers.EBX])
            else:
                prop_var = compiler.environment.get_local_var("var_%s_%s" % (obj_var, node.prop_name))
                if prop_var is None:
                    prop_var = compiler.environment.add_local_var(Types.INT, node.prop_name, object_namespace=obj_var)
                compiler.code.add(Commands.POP, prop_var)
    else:
        if node.object_name == 'this':
            prop_var = compiler.environment.get_parent_local_var("var_%s_%s" % (obj_var, node.prop_name))
            compiler.code.add(Commands.MOV, [Registers.EBX, "dword [%s]" % compiler.environment.object_list[-1][1]])
            compiler.code.add(Commands.SUB, [Registers.EBX, prop_var['offset']])
            compiler.code.add(Commands.PUSH, 'dword [%s]' % Registers.EBX)
        else:
            if compiler.environment.current is not None:
                prop_var = compiler.environment.get_parent_local_var("var_%s_%s" % (obj_var, node.prop_name))
                compiler.code.add(Commands.MOV, [Registers.EBX, "dword [%s]" % compiler.environment.object_list[-1][1]])
                compiler.code.add(Commands.SUB, [Registers.EBX, prop_var['offset']])
                compiler.code.add(Commands.PUSH, 'dword [%s]' % Registers.EBX)
            else:
                prop_var = compiler.environment.get_local_var("var_%s_%s" % (obj_var, node.prop_name))
                compiler.code.add(Commands.PUSH, prop_var)

    return compiler.types.set(Types.REFERENCE)


def object_method(compiler, node):
    if node.object_name == 'this':
        obj_var = compiler.environment.object_list[-1][0]
    else:
        if compiler.environment.current is not None:
            obj_var = compiler.environment.get_object_name(compiler.environment.get_parent_local_var(node.object_name, as_object=False))
        else:
            obj_var = compiler.environment.get_object_name(compiler.environment.get_local_var(node.object_name))

    new_node = copy(node)
    new_node.name = "o%s!%s" % (obj_var, node.method_name)

    return compile_call_statement(compiler, new_node)
