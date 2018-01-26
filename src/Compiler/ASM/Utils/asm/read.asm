read:
    mov     eax, 3
    push    255             ; read buffer size
    push    read_buffer     ; read buffer pointer
    push    0
    push    eax
    int     0x80
    add     esp, 16
    ret