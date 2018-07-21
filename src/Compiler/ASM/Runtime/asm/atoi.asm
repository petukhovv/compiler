%define ASCII_EOL       10
%define ASCII_ZERO      48
%define ASCII_MINUS     45

global atoi
atoi:
    ; zeroing the use of registers
    xor     eax, eax
    xor     bx, bx
    xor     cx, cx

    movzx   edx, word [read_buffer_offset]      ; setting offset (if some data has already been read before)
    add     edx, read_buffer                    ; placing the address on the read buffer in the edx register
    .atoi_start:
        mov     bl, byte [edx]                  ; place the next byte of read data in the bl register
        test    bl, bl                          ; zero check for read byte and exit if it's true
        jz      .atoi_exit
        inc     cx                              ; increment chars counter
        cmp     bl, ASCII_EOL                   ; EOL check (ASCII code 10) and exit if it's true
        je      .atoi_exit
        inc	    edx                             ; increment read buffer address (go to the next byte)
        cmp     bl, ASCII_MINUS                 ; minus check (ASCII code 45) and go to the negative mark if it's true
        je      .atoi_negative_mark
        imul    eax, 10                         ; go to the next digit (order) of the read number
        sub	    bl, ASCII_ZERO                  ; subtraction of the first number (0 with ASCII code 48) in ASCII symbols
        add	    al, bl                          ; writing the digit to the first order (guaranteed without overflow: first order al is 0, bl is 0..9)
        jmp	    .atoi_start
    .atoi_negative_mark:
        mov     bh, 1                           ; set negative number flag
        jmp	    .atoi_start
    .atoi_negative:
        neg     eax                             ; read number invert to negative
        xor     bh, bh                          ; zeroing the negative number flag
        jmp     .atoi_exit
    .atoi_exit:
        cmp     bh, 1                           ; check negative number flag and go to the invert to negative section if it's true
        je      .atoi_negative

        cmp     cx, [read_buffer_size]
        jnz     .atoi_write_buffer_offset
        mov     dword [read_buffer_offset], 0   ; the whole stdin is read, zeroing the offset
        ret

        .atoi_write_buffer_offset:
            add     [read_buffer_offset], cx    ; offset which equal of the read data size before the newline symbol (\n)
            ret
