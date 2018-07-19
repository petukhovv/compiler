global gc_decrease
gc_decrease:
    .gc_start:
        cmp		    eax, 0
        jle 	    .gc_finish          ; go to gc_finish if pointer is zero pointer or stack pointer
        jmp         .gc_decrement
    .gc_decrement:
        push        eax
        call  		gc_deep_decrease
        pop         eax
        sub		    eax, 2
        mov		    bx, word [eax]
        sub		    bx, 1               ; pointers counter decrement
        mov		    word [eax], bx
        add		    eax, 2
        cmp		    bx, 0
        jnz     	.gc_finish
        call  		free
        jmp     	.gc_finish
    .gc_finish:
        ret

global gc_increase
gc_increase:
    sub		    eax, 2              ; store pointers counter in first two bytes of heap object
    mov		    bx, word [eax]
    add		    bx, 1               ; pointers counter increment
    mov		    word [eax], bx
    add		    eax, 2
    cmp         ecx, 5              ; compare type to boxed array (id = 5)
    call  		gc_deep_increase
    ret

global gc_start_if_need
gc_start_if_need:
    cmp		    ebx, 5              ; compare type to boxed array (id = 5)
    jz  		gc_decrease.gc_start
    cmp		    ebx, 6              ; compare type to unboxed array (id = 6)
    jz  		gc_decrease.gc_start
    ret

gc_deep_decrease:
    mov         edx, eax
    mov         ecx, dword [edx]
    cmp		    ecx, 0
    jz  		.gc_continue
    ret
    .gc_continue:
        mov         eax, ecx
        mov         ebx, 8
        mul         ebx
        add         eax, 4
        add         edx, eax
        loop_elements:
            sub         edx, 4
            mov         eax, dword [edx]
            mov		    bx, word [eax - 2]
            sub		    bx, 1                   ; pointers counter increment
            mov		    word [eax - 2], bx

            sub         edx, 4
            mov         ebx, dword [edx]
            cmp         ebx, 5                  ; compare type to boxed array (id = 5)
            jnz  		.gc_deep_decrease_continue

            push        ecx
            push        edx
            push        eax
            call  		gc_deep_decrease
            pop         eax
            pop         edx
            pop         ecx
        .gc_deep_decrease_continue:
            call  		free
            loop        loop_elements
        ret

gc_deep_increase:
    mov         edx, eax
    mov         ecx, dword [edx]
    cmp		    ecx, 0
    jz  		.gc_continue
    ret
    .gc_continue:
        mov         eax, ecx
        mov         ebx, 8
        mul         ebx
        add         eax, 4
        add         edx, eax
        loop_by_elements:
            sub         edx, 4
            mov         eax, dword [edx]
            mov		    bx, word [eax - 2]
            add		    bx, 1                   ; pointers counter increment
            mov		    word [eax - 2], bx

            sub         edx, 4
            mov         ebx, dword [edx]
            cmp         ebx, 5                  ; compare type to boxed array (id = 5)
            jnz  		.gc_deep_increase_continue

            push        ecx
            push        edx
            call  		gc_deep_increase
            pop         edx
            pop         ecx
        .gc_deep_increase_continue:
            loop        loop_by_elements
        ret