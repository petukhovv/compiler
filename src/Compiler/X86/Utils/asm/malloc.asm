malloc:
    push ebp
    mov ebp,esp
    push eax
    call _malloc
    add esp,4
    pop ebp
    ret