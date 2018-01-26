from .Deep.arrays import *
from .Helpers.commands import Commands
from .Helpers.registers import Registers


def arrmake(compiler, args, type):
    """ Built-in arrmake (create unboxed arrays) / Arrmake (create boxed arrays) functions compilation """
    type = Types.BOXED_ARR if type == 'boxed' else Types.UNBOXED_ARR

    # When they passed default values (in second argument), we look, in what particular format
    if len(args.elements) == 2:
        default_value_type = args.elements[1].compile_asm(compiler)
        compiler.commands.clean_type()
        # If the second argument was passed [] or {}, then the duplicated element will be 0
        # ( signature: arrmake(n, []), Arrmake(n, {}) )
        if default_value_type == type and len(args.elements[1].elements.elements) == 0:
            # We clear the pointer to an empty array
            # TODO: after the implementation of the GC do here delete the array
            compiler.code.stack_pop()
            compiler.code.add(Commands.PUSH, [0])
            default_values_variant = 'zeros'
        # If the second argument was passed [n1, n2, ...] or {a1, a2, ...},
        # then the array is already created, just return the type and exit
        elif default_value_type == type:
            return compiler.commands.set_and_return_type(type)
        # If no array has been passed, but the number (or pointer), then it will be a duplicate element
        else:
            default_values_variant = 'repeated'
    # If nothing has been passed, then the elements of the array will be 0
    else:
        default_values_variant = 'none'

    args.elements[0].compile_asm(compiler)
    compiler.commands.clean_type()

    ArrayCompiler.arrmake(compiler, default_values_variant)

    return compiler.commands.set_and_return_type(type)


def arrmake_inline(compiler, elements, type):
    """ Compilation the inline construction to create boxed and unboxed arrays: [n1, n2, ...] / {a1, a2, ...} """
    type = Types.BOXED_ARR if type == 'boxed' else Types.UNBOXED_ARR

    arr_elements = elements.compile_asm(compiler)
    arr_length = len(arr_elements)
    arr_pointer = compiler.bss.vars.add(
        None,
        'resb',
        arr_length * 2 * 4 + 4,
        Types.INT if type == Types.BOXED_ARR else Types.DYNAMIC
    )

    compiler.code.add(Commands.MOV, ['dword [%s]' % arr_pointer, arr_length])
    for i, element in enumerate(arr_elements):
        element_place = i * 2 * 4 + 4

        if type == Types.BOXED_ARR:
            element_type = compiler.bss.vars.get_type(element)
            element = compiler.bss.vars.get(element)
            compiler.code.add(Commands.MOV, [Registers.EAX, element_type])
            compiler.code.add(Commands.MOV, [Registers.EBX, element])
            element_type = Registers.EAX
            element = Registers.EBX
        else:
            element_type = Types.DYNAMIC

        compiler.code.add(Commands.MOV, ['dword [%s+%d]' % (arr_pointer, element_place), element_type])
        compiler.code.add(Commands.MOV, ['dword [%s+%d]' % (arr_pointer, element_place + 4), element])

    compiler.code.add(Commands.PUSH, [arr_pointer])

    return compiler.commands.set_and_return_type(type)


def array_element(compiler, array, index, other_indexes, context):
    """ Compilation the get array element operator: A[n] """
    var_name = compiler.bss.vars.get(array)
    var_type = compiler.bss.vars.get_type(array)

    # Compilation obtain a pointer construction to the beginning of an array
    compiler.code.add(Commands.PUSH, [var_name])

    # Compilation obtain an index construction
    index.compile_asm(compiler)
    compiler.commands.clean_type()

    def other_index_compile(other_index):
        compiler.commands.clean_type()
        other_index.compile_asm(compiler)
        compiler.commands.clean_type()

    if context == 'assign':
        # If several consecutive indices, compile each
        if other_indexes is not None:
            for other_index in other_indexes:
                ArrayCompiler.get_element(compiler, var_type)
                other_index_compile(other_index)
        ArrayCompiler.set_element(compiler, var_type)
    else:
        ArrayCompiler.get_element(compiler, var_type)
        # If several consecutive indices, compile each
        if other_indexes is not None:
            for other_index in other_indexes:
                other_index_compile(other_index)
                ArrayCompiler.get_element(compiler, var_type)

    return Types.DYNAMIC


def arrlen(compiler, args):
    """ Built-in arrlen function compilation to get array length """
    args.elements[0].compile_asm(compiler)
    compiler.commands.clean_type()

    ArrayCompiler.arrlen(compiler)

    return compiler.commands.set_and_return_type(Types.INT)
