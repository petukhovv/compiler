_itoa:
    push eax
    push edx
    xor edx,edx
    div dword [_itoa_radix]
    test eax,eax
    je ._itoa_next
    call _itoa
._itoa_next:
    lea eax,[edx+'0']
    call _write
    pop edx
    pop eax
    ret