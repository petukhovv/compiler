EXTERN _malloc

global malloc
malloc:
    mov		ecx, eax    ; stack alignment start
    mov		eax, ebp
    sub		eax, esp
    xor		edx, edx
    mov		ebx, 16
    div		ebx
    mov		eax, 16
    sub		eax, edx
    add		eax, 12
    sub		esp, eax
    push	eax         ; stack alignment finish
    add		ecx, 2
    push	ecx
    call	_malloc
    mov		word [eax], 0
    add		eax, 2
    add		esp, 4
    pop		ebx         ; restore stack alignment start
    add		esp, ebx    ; restore stack alignment finish
    ret