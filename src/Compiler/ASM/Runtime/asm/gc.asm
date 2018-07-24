%define BOXED_ARRAY_TYPE_ID         5
%define UNBOXED_ARRAY_TYPE_ID       6

global gc_decrease
gc_decrease:
    .gc_start:                              ; decrease reference counter
        cmp		    eax, 0                  ; null-check pointer and stack addresses check (pointer <= 0)
        jle 	    .gc_finish              ; do not garbage collection if true
    .gc_decrement:
        sub		    eax, 2                  ; accounting for reservation of the 2 byte for reference count
        mov		    cx, word [eax]
        sub		    cx, 1                   ; reference counter decrement
        mov		    word [eax], cx
        add		    eax, 2                  ; restoring 2 byte for reference count

        cmp         ebx, BOXED_ARRAY_TYPE_ID    ; compare type to boxed array (id = 5), garbage collection is relevant only for it
        jnz     	.gc_skip_deep_decrease
        push        ecx
        call  		gc_deep_decrease        ; depth walk of the objects graph and decrement reference counters
        pop         ecx

    .gc_skip_deep_decrease:
        cmp		    cx, 0
        jnz     	.gc_finish              ; do not free memory if the reference count is not zero
        call  		free
    .gc_finish:
        ret

global gc_increase
gc_increase:
    sub		    eax, 2                      ; accounting for reservation of the 2 byte for reference count
    mov		    bx, word [eax]
    add		    bx, 1                       ; reference counter increment
    mov		    word [eax], bx
    add		    eax, 2                      ; restoring 2 byte for reference count
    cmp         ecx, BOXED_ARRAY_TYPE_ID    ; compare type to boxed array (id = 5), garbage collection is relevant only for it
    jnz     	.gc_finish
    call  		gc_deep_increase            ; depth walk of the objects graph and increment reference counters
    .gc_finish:
        ret

global gc_start_if_need
gc_start_if_need:                           ; run GC on boxed/unboxed arrays only
    cmp		    ebx, BOXED_ARRAY_TYPE_ID
    jz  		gc_decrease.gc_start
    cmp		    ebx, UNBOXED_ARRAY_TYPE_ID
    jz  		gc_decrease.gc_start
    ret

gc_deep_decrease:
    mov         edx, eax
    mov         ecx, dword [edx]
    cmp		    ecx, 0
    jnz  		.gc_continue
    ret
    .gc_continue:
        mov         eax, ecx
        mov         ebx, 8
        mov         esi, edx
        mul         ebx
        mov         edx, esi
        add         eax, 4
        add         edx, eax
        .loop_by_elements:
            sub         edx, 8
            mov         eax, dword [edx + 4]
            cmp         eax, 0
            jz  		.gc_deep_decrease_continue

            mov		    bx, word [eax - 2]
            sub		    bx, 1                   ; pointers counter decrement
            mov		    word [eax - 2], bx

            mov         ebx, dword [edx]
            cmp         ebx, BOXED_ARRAY_TYPE_ID                  ; compare type to boxed array (id = 5)
            jnz  		.gc_free

            push        ecx
            push        edx
            call  		gc_deep_decrease
            pop         edx
            pop         ecx
            mov         eax, dword [edx]
        .gc_free:
            mov		    bx, word [eax - 2]
            cmp         bx, 0
            jnz  		.gc_deep_decrease_continue
            call  		free
        .gc_deep_decrease_continue:
            loop        .loop_by_elements
        ret

gc_deep_increase:
    mov         edx, eax
    mov         ecx, dword [edx]
    cmp		    ecx, 0
    jnz  		.gc_continue
    ret
    .gc_continue:
        mov         eax, ecx
        mov         ebx, 8
        mov         esi, edx
        mul         ebx
        mov         edx, esi
        add         eax, 4
        add         edx, eax
        .loop_by_elements:
            sub         edx, 8
            mov         eax, dword [edx + 4]
            cmp         eax, 0
            jz  		.gc_deep_increase_continue

            mov		    bx, word [eax - 2]
            add		    bx, 1                   ; pointers counter increment
            mov		    word [eax - 2], bx

            mov         ebx, dword [edx]
            cmp         ebx, BOXED_ARRAY_TYPE_ID                  ; compare type to boxed array (id = 5)
            jnz  		.gc_deep_increase_continue

            push        ecx
            push        edx
            call  		gc_deep_increase
            pop         edx
            pop         ecx
        .gc_deep_increase_continue:
            loop        .loop_by_elements
        ret