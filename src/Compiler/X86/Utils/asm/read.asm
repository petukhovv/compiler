_read:
    mov eax, 3
    push dword [_read_buffer_size]
    push _read_buffer
    push 0
    push eax
    int 0x80
    add esp, 16
    ret