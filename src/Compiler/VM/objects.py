import sys

from .Helpers.types import Types
from .Helpers.commands import *

from .functions import function as compile_function
from .functions import call_statement as compile_call_statement

from copy import copy

objects = sys.modules['Parser.AST.objects']


def object_def(commands, data, node):
    object_var = data.create_var(type=Types.OBJECT)
    data.context_objects.append(object_var)

    for element in node.elements.elements:
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


def object_val_def(commands, data, node):
    prop_var = data.get_var(node.name.name, object_namespace=data.context_objects[-1])
    node.value.compile_vm(commands, data)
    commands.store_value(prop_var, type=Types.DYNAMIC)


def object_method_def(commands, data, node):
    new_node = copy(node)
    new_node.name = "o%s!%s" % (data.context_objects[-1], node.name)

    return compile_function(commands, data, new_node)


def object_val(commands, data, node):
    if node.object_name == 'this':
        obj_var = data.context_objects[-1]
    else:
        obj_var = data.get_object_name(data.get_var(node.object_name, is_root=True))

    prop_var = data.get_object_property(obj_var, node.prop_name, Types.DYNAMIC)

    if node.context == 'assign':
        commands.store_value(prop_var, type=Types.DYNAMIC, is_parent_scope=len(data.context_objects) > 0)
    else:
        commands.load_value(prop_var, is_parent_scope=len(data.context_objects) > 0)

    return Types.DYNAMIC


def object_method(commands, data, node):
    if node.object_name == 'this':
        obj_var = data.context_objects[-1]
    else:
        obj_var = data.get_object_name(data.get_var(node.object_name, is_root=True))

    new_node = copy(node)
    new_node.name = "o%s!%s" % (obj_var, node.method_name)

    return compile_call_statement(commands, data, new_node)
