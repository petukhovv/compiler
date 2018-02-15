global itoa
itoa:
    .itoa_start:
        test    eax, eax
        js      .itoa_print_minus
        push    eax
        push    edx
        xor     edx,edx
        mov     ebx, 10
        div     ebx
        test    eax,eax
        je      .itoa_next
        call    itoa
    .itoa_next:
        lea     eax,[edx+48]       ; 48 - ASCII code of 0
        call    write
        pop     edx
        pop     eax
        ret
    .itoa_print_minus:
        push    eax
        mov     eax, 45
        call    write
        pop     eax
        neg     eax
        jmp     .itoa_start