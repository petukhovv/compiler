import sys

from .Helpers.types import Types
from .Helpers.commands import *

objects = sys.modules['Parser.AST.objects']


def object_def(commands, data, elements):
    object_var = data.create_var(type=Types.OBJECT)
    data.defined_object = object_var
    data.context_objects.append(object_var)

    for element in elements.elements:
        if isinstance(element, objects.ObjectValDef):
            var = data.create_var(alias=element.name.name, type=Types.DYNAMIC, double_size=True, object_namespace=object_var)
            element.compile_vm(commands, data)
            commands.store_value(var, type=Types.DYNAMIC)

    data.context_objects.pop()
    commands.add(Push, object_var)

    return commands.set_and_return_type(Types.OBJECT)


def object_val_def(commands, data, name, value):
    prop_var = data.get_var(name.name, object_namespace=data.context_objects[-1])
    value.compile_vm(commands, data)
    commands.store_value(prop_var, type=Types.DYNAMIC)


def object_val(commands, data, object_name, prop_name, other_prop_names, context):
    prop_var = data.get_object_property(data.get_var(object_name), prop_name)

    if context == 'assign':
        commands.store_value(prop_var, type=Types.DYNAMIC)
    else:
        commands.load_value(prop_var)

    return Types.DYNAMIC
