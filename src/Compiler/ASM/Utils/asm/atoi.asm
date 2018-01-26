atoi:
    mov ebx, 0
    mov ecx, 0
    add esi, [read_buffer_done]
    .atoi_start:
        xor     edx, edx
        mov     dl, byte [esi]
        test    dl, dl
        jz      .atoi_exit
        add     ecx, 1
        cmp     dl, 10                  ; 10 - ASCII code of EOL (\n)
        je      .atoi_exit
        cmp     dl, 45                  ; 45 - ASCII code of - (minus - mark for negative value)
        je      .atoi_negative_mark
        imul    eax, 10
        sub	    dl, 48                  ; 48 - ASCII code of 0
        add	    eax, edx
        inc	    esi
        jmp	    .atoi_start
    .atoi_negative_mark:
        mov     ebx, 1
        inc	    esi
        jmp	    .atoi_start
    .atoi_negative:
        neg     eax
        mov     ebx, 0
        jmp     .atoi_exit
    .atoi_exit:
        cmp     ebx, 1
        je      .atoi_negative
        mov     dl, 0

        cmp     ecx, [read_buffer_all]
        jnz     .atoi_write_buffer_done
        mov     dword [read_buffer_done], 0
        jmp     .atoi_process_buffer_end

        .atoi_write_buffer_done:
            add     [read_buffer_done], ecx

        .atoi_process_buffer_end:
            ret