write:
    mov     [write_buffer], eax
    push    1
    push    write_buffer
    push    1
    mov     ebx, eax
    mov     eax, 4
    sub     esp, 4
    int     0x80
    mov     eax, ebx
    add     esp, 16
    ret