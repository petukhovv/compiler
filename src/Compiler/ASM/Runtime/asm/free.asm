EXTERN _free

global free
free:
    add		eax, 2

    mov		ebx, esp
    and		esp, -16		; stack alignment by 16 bytes
    sub		ebx, esp
    sub		esp, 8			; compensation of the following two push operations (for stack alignment)
    push	ebx				; store difference between an aligned stack and no

    push	eax				; push the required memory size
    call	_free
    mov		word [eax], 0	; zeroing the reference count (2 byte)
    add		eax, 2			; reservation of the 2 byte for reference count (make offset)

    add		esp, 4			; set a pointer to the second (from the end) pushed value (difference between an aligned stack and no) on the stack
    pop		ebx
    add		esp, ebx		; restore stack alignment
    add		esp, 8			; revert compensation of the two push operations before _malloc call

    ret