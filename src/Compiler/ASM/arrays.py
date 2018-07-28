from .Deep.arrays import *
from .Runtime.gc import GC


def arrmake(compiler, args, type):
    """ Built-in arrmake (create unboxed arrays) / Arrmake (create boxed arrays) functions compilation """
    type = Types.BOXED_ARR if type == 'boxed' else Types.UNBOXED_ARR

    # When they passed default values (in second argument), we look, in what particular format
    if len(args.elements) == 2:
        default_value_type = args.elements[1].compile_asm(compiler)
        compiler.types.pop()
        # If the second argument was passed [] or {}, then the duplicated element will be 0
        # ( signature: arrmake(n, []), Arrmake(n, {}) )
        if default_value_type == type and len(args.elements[1].elements.elements) == 0:
            # We clear the pointer to an empty array
            compiler.code.stack_pop()
            compiler.code.add(Commands.PUSH, 0)
            default_values_variant = 'zeros'
        # If the second argument was passed [n1, n2, ...] or {a1, a2, ...},
        # then the array is already created, just return the type and exit
        elif default_value_type == type:
            return compiler.types.set(type)
        # If no array has been passed, but the number (or pointer), then it will be a duplicate element
        else:
            # If the array is boxed and default pointer is not specified, then default pointer will be a 0
            if type == Types.BOXED_ARR:
                compiler.code.stack_pop()
                compiler.code.add(Commands.PUSH, 0)
            default_values_variant = 'repeated'
    # If nothing has been passed, then the elements of the array will be 0
    else:
        default_values_variant = 'none'

    args.elements[0].compile_asm(compiler)
    compiler.types.pop()

    ArrayCompiler.arrmake(compiler, default_values_variant)

    return compiler.types.set(type)


def arrmake_inline(compiler, elements, type):
    """ Compilation the inline construction to create boxed and unboxed arrays: [n1, n2, ...] / {a1, a2, ...} """
    type = Types.BOXED_ARR if type == 'boxed' else Types.UNBOXED_ARR

    arr_elements = elements.compile_asm(compiler)
    arr_length = len(arr_elements)
    arr_size = arr_length * 2 * 4 + 4
    if arr_length == 0:
        compiler.code.add(Commands.PUSH, 0)
        return type
    arr_pointer = compiler.environment.add_local_var(size=arr_size)

    compiler.code.add(Commands.MOV, [Registers.EAX, arr_pointer['pointer']]) \
        .add(Commands.ADD, [Registers.EAX, -arr_pointer['offset'] - arr_size]) \
        .add(Commands.MOV, ['dword [%s-%d]' % (arr_pointer['pointer'], arr_pointer['offset']), Registers.EAX])

    for i, element in enumerate(reversed(arr_elements)):
        element_place = i * 2 * 4 + 4

        if type == Types.BOXED_ARR:
            element_type = compiler.environment.get_local_var_type(element)
            element = compiler.environment.get_local_var(element)
            compiler.code.add(Commands.MOV, [Registers.EAX, element_type])
            compiler.code.add(Commands.MOV, [Registers.EBX, element])
            element_type = Registers.EAX
            element = Registers.EBX
        else:
            element_static_type = compiler.types.get_static_type(element)
            element_type = element_static_type\
                if element_static_type else compiler.environment.get_local_var_type(element)

        compiler.code.add(Commands.MOV, ['dword [%s-%d]' % (arr_pointer['pointer'], element_place + arr_pointer['offset']), element])\
            .add(Commands.MOV, ['dword [%s-%d]' % (arr_pointer['pointer'], element_place + arr_pointer['offset'] + 4), element_type])

        compiler.code.add(Commands.MOV, ['dword [%s-%d]' % (arr_pointer['pointer'], arr_pointer['offset'] + arr_size), arr_length])\
            .add(Commands.MOV, [Registers.EAX, 'dword [%s-%d]' % (arr_pointer['pointer'], arr_pointer['offset'])]) \
            .add(Commands.PUSH, Registers.EAX)

    return compiler.types.set(type)


def array_element(compiler, array, index, other_indexes, context, value_type):
    """ Compilation the get array element operator: A[n] """
    var_name = compiler.environment.get_local_var(array)
    var_type = compiler.environment.get_local_var_type(array)

    if context == 'assign':
        compiler.code.add(Commands.MOV, [Registers.EAX, 'dword [%s + 4]' % Registers.ESP])
        compiler.code.add(Commands.MOV, [Registers.EBX, 'dword [%s]' % Registers.ESP])
        GC(compiler).increment()

    # Compilation obtain a pointer construction to the beginning of an array
    compiler.code.add(Commands.PUSH, var_name)

    # Compilation obtain an index construction
    index.compile_asm(compiler)
    compiler.types.pop()

    def other_index_compile(other_index):
        compiler.types.pop()
        other_index.compile_asm(compiler)
        compiler.types.pop()

    if context == 'assign':
        # If several consecutive indices, compile each
        if other_indexes is not None:
            for other_index in other_indexes:
                ArrayCompiler.get_element(compiler, var_type)
                other_index_compile(other_index)

        ArrayCompiler.calc_element_place(compiler)

        compiler.code.add(Commands.MOV, [Registers.EAX, 'dword [%s + %s]' % (Registers.EBX, ArrayCompiler.ELEMENT_SIZE)])
        GC(compiler).decrement()

        compiler.code.add(Commands.POP, Registers.EAX)
        ArrayCompiler.set_element(compiler)
    else:
        ArrayCompiler.get_element(compiler, var_type)
        # If several consecutive indices, compile each
        if other_indexes is not None:
            for other_index in other_indexes:
                other_index_compile(other_index)
                ArrayCompiler.get_element(compiler, var_type)

    return var_type


def arrlen(compiler, args):
    """ Built-in arrlen function compilation to get array length """
    args.elements[0].compile_asm(compiler)
    compiler.types.pop()

    ArrayCompiler.arrlen(compiler)

    return compiler.types.set(Types.INT)
