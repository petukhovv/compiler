def __fill_array(arr, count, default_value):
    index = 0
    while index < count:
        arr.append(default_value)
        index += 1
    return arr


class UnboxedArrayWrap(list):
    pass


class BoxedArrayWrap(list):
    pass
