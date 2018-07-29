from ...Core.types import Types
from ...Core.commands import Commands
from ...Core.registers import Registers
from Parser.AST.declarations.property import ObjectValDef


def object_def(compiler, node):
    object_number = compiler.environment.add_object()
    obj_ebp_pointer = compiler.vars.add(None, "resb", Types.SIZE)
    compiler.code.add(Commands.MOV, ["dword [%s]" % obj_ebp_pointer, Registers.EBP])

    compiler.environment.object_list.append((object_number, obj_ebp_pointer))

    for element in node.elements.elements:
        if isinstance(element, ObjectValDef):
            prop_val = compiler.environment.add_local_var(Types.REFERENCE, element.name.name, object_namespace=object_number)
            element.compile_asm(compiler)
            compiler.code.add(Commands.POP, prop_val)
        else:
            element.compile_asm(compiler)

    compiler.environment.object_list.pop()
    compiler.code.add(Commands.PUSH, object_number)
    compiler.environment.defined_object = object_number

    return compiler.types.set(Types.REFERENCE)
