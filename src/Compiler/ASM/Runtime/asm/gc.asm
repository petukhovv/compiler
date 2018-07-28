%define BOXED_ARRAY_TYPE_ID         5
%define UNBOXED_ARRAY_TYPE_ID       6

SECTION .data
    cyclic_detected_warning:        db "WARNING: cyclic object pointers detected. Cyclic garbage collection is not supported.", 10
    cyclic_detected_warning_len:	equ $-cyclic_detected_warning

; MAX POINTERS: 2^15 - 1 = 32.768

SECTION .text
    global gc_increment
    gc_increment:
        cmp         ebx, BOXED_ARRAY_TYPE_ID        ; compare type to boxed array (id = 5), garbage collection is relevant only for reference values
        jz     	    .reference_value
        cmp         ebx, UNBOXED_ARRAY_TYPE_ID      ; compare type to boxed array (id = 6), garbage collection is relevant only for reference values
        jz     	    .reference_value
        jmp         .return                         ; if obtained value is not reference then go to return
        .reference_value:
            cmp		    eax, 0                      ; check null pointer and stack addresses check (pointer <= 0)
            jle 	    .return                     ; do not garbage collection if true

            mov		    cx, word [eax - 2]
            add		    cx, 1                       ; reference counter increment
            bts         cx, 15                      ; set depth walk bit (to detecting cyclic object pointers)
            mov		    word [eax - 2], cx

            cmp         ebx, BOXED_ARRAY_TYPE_ID    ; deep walk only for boxed arrays
            jnz     	.finalyze
            push        eax
            call  		gc_deep_increment
            pop         eax
        .finalyze:
            mov		    bx, word [eax - 2]
            btr         bx, 15                      ; reset depth walk bit
            mov		    word [eax - 2], bx
        .return:
            ret

    global gc_decrement
    gc_decrement:
        cmp		    ebx, BOXED_ARRAY_TYPE_ID        ; compare type to boxed array (id = 6), garbage collection is relevant only for reference values
        jz  		.reference_value
        cmp		    ebx, UNBOXED_ARRAY_TYPE_ID      ; compare type to boxed array (id = 6), garbage collection is relevant only for reference values
        jz  		.reference_value
        jmp         .return                         ; if obtained value is not reference then go to return
        .reference_value:
            cmp		    eax, 0                      ; check null pointer and stack addresses check (pointer <= 0)
            jle 	    .return                     ; do not garbage collection if true

            mov		    cx, word [eax - 2]
            sub		    cx, 1                       ; reference counter decrement
            bts         cx, 15                      ; set depth walk bit (to detecting cyclic object pointers)
            mov		    word [eax - 2], cx

            cmp         ebx, BOXED_ARRAY_TYPE_ID    ; deep walk only for boxed arrays
            jnz     	.finalyze
            push        eax
            call  		gc_deep_decrement
            pop         eax
        .finalyze:
            mov		    cx, word [eax - 2]
            btr         cx, 15                      ; reset depth walk bit
            mov		    word [eax - 2], cx

            cmp		    cx, 0
            jnz     	.return                     ; do not free memory if the reference count is not zero
            call  		free
        .return:
            ret

    gc_deep_decrement:
        mov         esi, eax                        ; save pointer to array
        mov         ecx, dword [esi]                ; array elements number write to the loop counter (ECX)
        cmp		    ecx, 0                          ; check array elements number
        jz  		near .return                    ; if 0 then return

        mov         eax, ecx
        mov         ebx, 8
        mul         ebx
        add         eax, 4                          ; calc array memory size (bytes): elements_number * 8 (4 byte for type + 4 byte for value) + 4 (elements number info)
        add         esi, eax                        ; calc pointer to the end of array (iterate from the end of array)
        .loop_by_elements:
            sub         esi, 8                      ; set pointer to the next element
            mov         eax, dword [esi + 4]
            cmp         eax, 0                      ; check null pointer and stack addresses check (pointer <= 0)
            jle  		.continue                   ; skip if true

            mov		    bx, word [eax - 2]
            bt          bx, 15                      ; check depth walk bit (to detecting cyclic object pointers)
            jc  		.cycle_pointers_warning     ; print warning if found cyclic object pointers
            sub		    bx, 1                       ; reference counter decrement
            bts         bx, 15                      ; set depth walk bit (to detecting cyclic object pointers)
            mov		    word [eax - 2], bx

            mov         ebx, dword [esi]
            cmp         ebx, BOXED_ARRAY_TYPE_ID    ; deep walk only for boxed arrays
            jnz  		.finalyze

            push        ecx                         ; save loop counter
            push        esi                         ; save pointer to array
            call  		gc_deep_decrement
            pop         esi
            pop         ecx
            mov         eax, dword [esi + 4]
        .finalyze:
            mov		    bx, word [eax - 2]
            btr         bx, 15                      ; reset depth walk bit
            mov		    word [eax - 2], bx
            cmp         bx, 0
            jnz  		.continue                   ; do not free memory if the reference count is not zero

            push        ecx                         ; save loop counter
            push        esi                         ; save pointer to array
            call  		free
            pop         esi
            pop         ecx
            jmp         .continue
        .cycle_pointers_warning:
            mov         eax, cyclic_detected_warning
            mov         ebx, cyclic_detected_warning_len
            call        write_error                 ; print warning about found cyclic object pointers
        .continue:
            loop        .loop_by_elements
        .return:
            ret

    gc_deep_increment:
        mov         esi, eax                        ; save pointer to array
        mov         ecx, dword [esi]                ; array elements number write to the loop counter (ECX)
        cmp		    ecx, 0                          ; check array elements number
        jz  		.return                         ; if 0 then return

        mov         eax, ecx
        mov         ebx, 8
        mul         ebx
        add         eax, 4                          ; calc array memory size (bytes): elements_number * 8 (4 byte for type + 4 byte for value) + 4 (elements number info)
        add         esi, eax                        ; calc pointer to the end of array (iterate from the end of array)
        .loop_by_elements:
            sub         esi, 8                      ; set pointer to the next element
            mov         eax, dword [esi + 4]
            cmp         eax, 0                      ; check null pointer and stack addresses check (pointer <= 0)
            jle  		.continue                   ; skip if true

            mov		    bx, word [eax - 2]
            bt          bx, 15                      ; check depth walk bit (to detecting cyclic object pointers)
            jc  		.continue                   ; skip if found cyclic object pointers
            add		    bx, 1                       ; reference counter increment
            bts         bx, 15                      ; set depth walk bit (to detecting cyclic object pointers)
            mov		    word [eax - 2], bx

            mov         ebx, dword [esi]
            cmp         ebx, BOXED_ARRAY_TYPE_ID    ; deep walk only for boxed arrays
            jnz  		.finalyze

            push        ecx                         ; save loop counter
            push        esi                         ; save pointer to array
            call  		gc_deep_increment
            pop         esi
            pop         ecx
        .finalyze:
            mov         eax, dword [esi + 4]
            mov		    bx, word [eax - 2]
            btr         bx, 15                      ; reset depth walk bit
            mov		    word [eax - 2], bx
        .continue:
            loop        .loop_by_elements
        .return:
            ret