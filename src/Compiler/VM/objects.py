import sys

from .Helpers.types import Types
from .Helpers.commands import *

from .functions import function as compile_function
from .functions import call_statement as compile_call_statement

objects = sys.modules['Parser.AST.objects']


def object_def(commands, data, elements):
    object_var = data.create_var(type=Types.OBJECT)
    data.context_objects.append(object_var)

    for element in elements.elements:
        if isinstance(element, objects.ObjectValDef):
            var = data.create_var(alias=element.name.name, type=Types.DYNAMIC, double_size=True, object_namespace=object_var)
            element.compile_vm(commands, data)
            commands.store_value(var, type=Types.DYNAMIC)
        else:
            element.compile_vm(commands, data)

    data.context_objects.pop()
    commands.add(Push, object_var)
    data.defined_object = object_var

    return commands.set_and_return_type(Types.OBJECT)


def object_val_def(commands, data, name, value):
    prop_var = data.get_var(name.name, object_namespace=data.context_objects[-1])
    value.compile_vm(commands, data)
    commands.store_value(prop_var, type=Types.DYNAMIC)


def object_method_def(commands, data, name, args, body):
    return compile_function(commands, data, "o%s!%s" % (data.context_objects[-1], name), args, body)


def object_val(commands, data, object_name, prop_name, other_prop_names, context):
    if object_name == 'this':
        obj_var = data.context_objects[-1]
    else:
        obj_var = data.get_object_name(data.get_var(object_name))

    prop_var = data.get_object_property(obj_var, prop_name, Types.DYNAMIC)

    if context == 'assign':
        commands.store_value(prop_var, type=Types.DYNAMIC, is_parent_scope=object_name == 'this')
    else:
        commands.load_value(prop_var, is_parent_scope=object_name == 'this')

    return Types.DYNAMIC


def object_method(commands, data, object_name, method_name, args):
    return compile_call_statement(commands, data, "o%s!%s" % (data.get_object_name(data.get_var(object_name)), method_name), args)
