class Data:
    @staticmethod
    def clone_string(pointer, current_data, new_data, new_stack):
        heap_offset = pointer
        current_symbol = None
        start_pointer = len(new_data['heap'])
        while current_symbol != 0:
            current_symbol = current_data['heap'][heap_offset]
            new_data['heap'].append(current_symbol)
            heap_offset += 1
        new_stack.append(start_pointer)
        new_stack.append(4)

    @staticmethod
    def clone_unboxed_array(pointer, current_data, new_data, new_stack):
        arrlen = current_data['heap'][pointer]
        start_pointer = len(new_data['heap'])
        arr_counter = 0
        while arr_counter <= arrlen:
            current_symbol = current_data['heap'][pointer + arr_counter]
            new_data['heap'].append(current_symbol)
            arr_counter += 1
        new_stack.append(start_pointer)
        new_stack.append(6)
