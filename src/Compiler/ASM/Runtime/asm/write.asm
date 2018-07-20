SECTION .text
    global write
    write:
        push    eax
        mov     ebx, esp
        push    1
        push    ebx
        push    1
        mov     eax, 4
        sub     esp, 4
        int     0x80
        add     esp, 20
        ret