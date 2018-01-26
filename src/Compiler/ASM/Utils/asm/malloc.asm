malloc:
    push    ebp
    mov     ebp, esp
    push  eax
    call _malloc
    mov     esp, ebp
    pop     ebp
    ret