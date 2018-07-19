EXTERN _malloc

global malloc
malloc:
    add		eax, 2

    mov     ecx, esp
    and     esp, -16        ; stack alignment
    sub     ecx, esp
    sub     esp, 8
    push	ecx             ; store stack aligned diff

    push	eax
    call	_malloc
    mov		word [eax], 0
    add		eax, 2

    add		esp, 4
    pop     ecx             ; restore stack aligned diff
    add		esp, ecx        ; restore stack alignment
    add		esp, 8

    ret