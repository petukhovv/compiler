%define ASCII_ZERO      48
%define ASCII_MINUS     45

global itoa_and_write
itoa_and_write:
    .itoa_start:
        test    eax, eax                ; this test uses the SF flag (significant bit check)
        js      .itoa_print_minus       ; if the first bit is 1 (SF=1), then the number is negative (go to the print minus section)
        xor     edx, edx                ; zeroing EDX (division remainder is written in it)
        mov     ebx, 10                 ; 10 is a divisor (because we output the values in the decimal system)
        div     ebx                     ; the division of EAX by 10
        push    edx                     ; storing a division remainder (it correspond to the digits that we will output in the reverse order)
        test    eax, eax                ; check that the quotient is 0 (this test uses the ZF flag)
        je      .itoa_next              ; expanding recursion: printing ascii symbols, that correspond to the division remainders
        call    itoa_and_write          ; recursive call to process next symbol
    .itoa_next:
        pop     edx                     ; get previously stored division remainders
        lea     eax, [edx + ASCII_ZERO] ; convert division remainder to the ascii symbol code
        call    write
        ret                             ; recursive return
    .itoa_print_minus:
        mov     ebx, eax                ; storing a EAX (because write already use EAX)
        mov     eax, ASCII_MINUS
        call    write
        mov     eax, ebx                ; restoring a EAX
        neg     eax                     ; number invert to negative
        jmp     .itoa_start             ; continue process symbols
