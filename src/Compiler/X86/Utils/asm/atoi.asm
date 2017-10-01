_atoi:
    mov ebx, 0
    ._atoi_start:
        xor	edx, edx
        mov	dl, byte [esi]
        test	dl, dl
        jz	._atoi_exit
        cmp dl, 10          ; 10 - ASCII code of EOL (\n)
        je ._atoi_exit
        cmp dl, 45          ; 10 - ASCII code of -
        je ._atoi_invert_mark
        imul	eax, 10
        sub	dl, 48          ; 48 - ASCII code of 0
        add	eax, edx
        inc	esi
        jmp	._atoi_start
._atoi_invert_mark:
    mov ebx, 1
    inc	esi
    jmp	._atoi_start
._atoi_invert:
    neg eax
    mov ebx, 0
    jmp ._atoi_exit
._atoi_exit:
    cmp ebx, 1
    je ._atoi_invert
    mov dl, 0
	ret