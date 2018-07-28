%define BOXED_ARRAY_TYPE_ID         5
%define UNBOXED_ARRAY_TYPE_ID       6

SECTION .data
    cyclic_detected_warning:        db "WARNING: cyclic object pointers detected. Cyclic garbage collection is not supported.", 10
    cyclic_detected_warning_len:	equ $-cyclic_detected_warning

SECTION .text
    global gc_increment
    gc_increment:
        cmp         ebx, BOXED_ARRAY_TYPE_ID    ; compare type to boxed array (id = 5), garbage collection is relevant only for it
        jz     	    .reference_value
        cmp         ebx, UNBOXED_ARRAY_TYPE_ID    ; compare type to boxed array (id = 5), garbage collection is relevant only for it
        jz     	    .reference_value
        jmp         .return
        .reference_value:
            cmp		    eax, 0                  ; null-check pointer and stack addresses check (pointer <= 0)
            jle 	    .return              ; do not garbage collection if true

            mov		    cx, word [eax - 2]
            add		    cx, 1                       ; reference counter increment
            bts         cx, 15
            mov		    word [eax - 2], cx
            cmp         ebx, BOXED_ARRAY_TYPE_ID    ; compare type to boxed array (id = 5), garbage collection is relevant only for it
            jnz     	.finalyze
            push        eax
            call  		gc_deep_increment            ; depth walk of the objects graph and increment reference counters
            pop         eax
        .finalyze:
            mov		    bx, word [eax - 2]
            btr         bx, 15
            mov		    word [eax - 2], bx
        .return:
            ret

    global gc_decrement
    gc_decrement:
        cmp		    ebx, BOXED_ARRAY_TYPE_ID
        jz  		.reference_value
        cmp		    ebx, UNBOXED_ARRAY_TYPE_ID
        jz  		.reference_value
        jmp         .return
        .reference_value:
            cmp		    eax, 0                  ; null-check pointer and stack addresses check (pointer <= 0)
            jle 	    .return              ; do not garbage collection if true

            mov		    cx, word [eax - 2]
            sub		    cx, 1                   ; reference counter decrement
            bts         cx, 15
            mov		    word [eax - 2], cx

            cmp         ebx, BOXED_ARRAY_TYPE_ID    ; compare type to boxed array (id = 5), garbage collection is relevant only for it
            jnz     	.finalyze
            push        eax
            call  		gc_deep_decrement        ; depth walk of the objects graph and decrement reference counters
            pop         eax
        .finalyze:
            mov		    cx, word [eax - 2]
            btr         cx, 15
            mov		    word [eax - 2], cx
            cmp		    cx, 0
            jnz     	.return              ; do not free memory if the reference count is not zero
            call  		free
        .return:
            ret

    gc_deep_decrement:
        mov         edx, eax
        mov         ecx, dword [edx]
        cmp		    ecx, 0
        jnz  		.not_null_value
        ret
        .not_null_value:
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
            jz  		.continue

            mov		    bx, word [eax - 2]

            bt          bx, 15
            jc  		.cycle_pointers_warning

            sub		    bx, 1                   ; pointers counter decrement
            bts         bx, 15
            mov		    word [eax - 2], bx

            mov         ebx, dword [edx]
            cmp         ebx, BOXED_ARRAY_TYPE_ID                  ; compare type to boxed array (id = 5)
            jnz  		.free

            push        ecx
            push        edx
            call  		gc_deep_decrement
            pop         edx
            pop         ecx
            mov         eax, dword [edx + 4]
        .free:
            mov		    bx, word [eax - 2]
            btr         bx, 15
            mov		    word [eax - 2], bx
            cmp         bx, 0
            jnz  		.continue
            push        ecx
            push        edx
            call  		free
            pop         edx
            pop         ecx
            jmp         .continue
        .cycle_pointers_warning:
            mov         eax, cyclic_detected_warning
            mov         ebx, cyclic_detected_warning_len
            call        write_error
        .continue:
            loop        .loop_by_elements
            ret

    gc_deep_increment:
        mov         edx, eax
        mov         ecx, dword [edx]
        cmp		    ecx, 0
        jnz  		.not_null_value
        ret
        .not_null_value:
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
            jz  		.continue

            mov		    bx, word [eax - 2]

            bt          bx, 15
            jc  		.continue

            add		    bx, 1                   ; pointers counter increment
            bts         bx, 15
            mov		    word [eax - 2], bx

            mov         ebx, dword [edx]
            cmp         ebx, BOXED_ARRAY_TYPE_ID                  ; compare type to boxed array (id = 5)
            jnz  		.finalyze

            push        ecx
            push        edx
            call  		gc_deep_increment
            pop         edx
            pop         ecx
        .finalyze:
            mov         eax, dword [edx + 4]
            mov		    bx, word [eax - 2]
            btr         bx, 15
            mov		    word [eax - 2], bx
        .continue:
            loop        .loop_by_elements
            ret