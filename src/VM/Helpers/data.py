from pprint import pprint

class Data:
    @staticmethod
    def clone_string(pointer, current_scope, new_scope, stack):
        heap_offset = pointer
        current_symbol = None
        start_pointer = len(new_scope.heap)
        while current_symbol != 0:
            current_symbol = current_scope.heap[heap_offset]
            new_scope.heap.append(current_symbol)
            heap_offset += 1
        stack.append(4)
        stack.append(start_pointer)

    @staticmethod
    def clone_string_inline(pointer, current_scope, new_scope, stack):
        stack_offset = pointer
        current_symbol = None
        start_pointer = len(new_scope.heap)
        while current_symbol != 0:
            current_symbol = current_scope.stack[stack_offset]
            new_scope.heap.append(current_symbol)
            stack_offset += 1
        stack.append(4)
        stack.append(start_pointer)

    @staticmethod
    def clone_unboxed_array(pointer, current_scope, new_scope, stack):
        arrlen = current_scope.heap[pointer]
        start_pointer = len(new_scope.heap)
        arr_counter = 0
        while arr_counter <= arrlen:
            current_symbol = current_scope.heap[pointer + arr_counter]
            new_scope.heap.append(current_symbol)
            arr_counter += 1
        stack.append(6)
        stack.append(start_pointer)

    @staticmethod
    def clone_unboxed_inline_array(pointer, current_scope, new_scope, stack):
        arrlen = current_scope.stack[pointer]
        start_pointer = len(new_scope.heap)
        arr_counter = 0
        while arr_counter <= arrlen:
            current_symbol = current_scope.stack[pointer + arr_counter]
            new_scope.heap.append(current_symbol)
            arr_counter += 1
        stack.append(6)
        stack.append(start_pointer)
