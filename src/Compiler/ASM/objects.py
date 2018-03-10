import sys

from .Core.types import Types
from .Core.commands import Commands
from .Core.registers import Registers

from .functions import function as compile_function
from .functions import call_statement as compile_call_statement


objects = sys.modules['Parser.AST.objects']


def object_def(compiler, elements):
    object_number = compiler.environment.add_object()
    obj_ebp_pointer = compiler.environment.add_local_var(type=Types.INT)
    compiler.code.add(Commands.MOV, [obj_ebp_pointer, Registers.EBP])

    compiler.environment.object_list.append((object_number, obj_ebp_pointer))

    for element in elements.elements:
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


def object_val_def(compiler, name, value):
    value_type = value.compile_asm(compiler)

    prop_var = compiler.environment.add_local_var(Types.INT, name.name, object_namespace=compiler.environment.object_list[-1][0])
    compiler.code.add(Commands.POP, prop_var)


def object_method_def(compiler, name, args, body):
    return compile_function(compiler, "o%s!%s" % (compiler.environment.object_list[-1][0], name), args, body)


def object_val(compiler, object_name, prop_name, other_prop_names, context):
    if object_name == 'this':
        obj_var = compiler.environment.object_list[-1][0]
    else:
        obj_var = compiler.environment.get_object_name(compiler.environment.get_local_var(object_name))

    prop_var = compiler.environment.get_local_var("var_%s_%s" % (obj_var, prop_name))

    if context == 'assign':
        if object_name == 'this':
            prop_var = compiler.environment.get_parent_local_var("var_%s_%s" % (obj_var, prop_name))
            compiler.code.add(Commands.MOV, [Registers.EBX, compiler.environment.object_list[-1][1]])
            compiler.code.add(Commands.SUB, [Registers.EBX, prop_var['offset']])
            compiler.code.add(Commands.POP, 'dword [%s]' % Registers.EBX)
        else:
            compiler.code.add(Commands.POP, prop_var)
    else:
        compiler.code.add(Commands.PUSH, prop_var)
        compiler.code.add(Commands.PUSH, Types.REFERENCE)


def object_method(compiler, object_name, method_name, args):
    obj_var = compiler.environment.get_object_name(compiler.environment.get_local_var(object_name))

    return compile_call_statement(compiler, "o%s!%s" % (obj_var, method_name), args)
