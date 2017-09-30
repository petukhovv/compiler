printChar:
    mov [_char], eax
    push 1
    push _char
    push 1
    mov ebx, eax
    mov eax, 4
    sub esp, 4
    int 0x80
    mov eax, ebx
    add esp, 16
    ret
itoa:
    push eax
    push edx
    xor edx,edx
    div dword [_itoa_radix]
    test eax,eax
    je .itoa_next
    call itoa
.itoa_next:
    lea eax,[edx+'0']
    call printChar
    pop edx
    pop eax
    ret