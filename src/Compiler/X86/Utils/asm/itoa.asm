_itoa:
    ._itoa_start:
        test eax, eax
        js ._itoa_print_minus
        push eax
        push edx
        xor edx,edx
        div dword [_itoa_radix]
        test eax,eax
        je ._itoa_next
        call _itoa
    ._itoa_next:
        lea eax,[edx+48]       ; 48 - ASCII code of 0
        call _write
        pop edx
        pop eax
        ret
    ._itoa_print_minus:
        push eax
        mov eax, 45
        call _write
        pop eax
        neg eax
        jmp ._itoa_start