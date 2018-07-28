import sys

from .Core.types import Types
from .Core.commands import Commands
from .Core.registers import Registers

from copy import copy

from .functions import function as compile_function
from .functions import call_statement as compile_call_statement


objects = sys.modules['Parser.AST.objects']


def object_def(compiler, node):
    object_number = compiler.environment.add_object()
    obj_ebp_pointer = compiler.vars.add(None, "resb", Types.SIZE)
    compiler.code.add(Commands.MOV, ["dword [%s]" % obj_ebp_pointer, Registers.EBP])

    compiler.environment.object_list.append((object_number, obj_ebp_pointer))

    for element in node.elements.elements:
        if isinstance(element, objects.ObjectValDef):
            prop_val = compiler.environment.add_local_var(Types.REFERENCE, element.name.name, object_namespace=object_number)
            element.compile_asm(compiler)
            compiler.code.add(Commands.POP, prop_val)
        else:
            element.compile_asm(compiler)

    compiler.environment.object_list.pop()
    compiler.code.add(Commands.PUSH, object_number)
    compiler.environment.defined_object = object_number

    return compiler.types.set(Types.REFERENCE)


def object_val_def(compiler, node):
    value_type = node.value.compile_asm(compiler)

    prop_var = compiler.environment.add_local_var(value_type, node.name.name, object_namespace=compiler.environment.object_list[-1][0])
    compiler.code.add(Commands.POP, prop_var)


def object_method_def(compiler, node):
    new_node = copy(node)
    new_node.name = "o%s!%s" % (compiler.environment.object_list[-1][0], node.name)

    return compile_function(compiler, new_node)


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
