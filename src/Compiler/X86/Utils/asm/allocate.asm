_allocate:
    mov    eax, 45                  ; system call brk
    pop    ebx                      ; write bytes number from stack (for allocate)
    add    ebx, [current_break]
    int    0x80
    mov    [new_break], eax
    mov    [current_break], eax
    ret