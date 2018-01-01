_atoi:
    mov ebx, 0
    mov ecx, 0
    add esi, [_read_buffer_done]
    ._atoi_start:
        xor	edx, edx
        mov	dl, byte [esi]
        test dl, dl
        jz ._atoi_exit
        add ecx, 1
        cmp dl, 10          ; 10 - ASCII code of EOL (\n)
        je ._atoi_exit
        cmp dl, 45          ; 45 - ASCII code of - (minus - mark for negative value)
        je ._atoi_negative_mark
        imul eax, 10
        sub	dl, 48          ; 48 - ASCII code of 0
        add	eax, edx
        inc	esi
        jmp	._atoi_start
    ._atoi_negative_mark:
        mov ebx, 1
        inc	esi
        jmp	._atoi_start
    ._atoi_negative:
        neg eax
        mov ebx, 0
        jmp ._atoi_exit
    ._atoi_exit:
        cmp ebx, 1
        je ._atoi_negative
        mov dl, 0

        cmp ecx, [_read_buffer_all]
        jnz ._atoi_write_buffer_done
        mov dword [_read_buffer_done], 0
        jmp ._atoi_process_buffer_end

        ._atoi_write_buffer_done:
            add [_read_buffer_done], ecx

        ._atoi_process_buffer_end:
            ret