from ...Helpers.types import Types
from ...Helpers.commands import Push
from Parser.AST.declarations.property import ObjectValDef


def object_def(commands, data, node):
    object_var = data.create_var(type=Types.OBJECT)
    data.context_objects.append(object_var)

    for element in node.elements.elements:
        if isinstance(element, ObjectValDef):
            var = data.create_var(alias=element.name.name, type=Types.DYNAMIC, double_size=True, object_namespace=object_var)
            element.compile_vm(commands, data)
            commands.store_value(var, type=Types.DYNAMIC)
        else:
            element.compile_vm(commands, data)

    data.context_objects.pop()
    commands.add(Push, object_var)
    data.defined_object = object_var

    return commands.set_and_return_type(Types.OBJECT)
