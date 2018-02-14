gc:
    .gc_start:
        cmp		    eax, 0
        jle 	    .gc_finish          ; go to gc_finish if pointer is zero pointer or stack pointer
        sub		    eax, 2
        mov		    bx, word [eax]
        sub		    bx, 1               ; pointers counter decrement
        mov		    word [eax], bx
        cmp		    bx, 0
        jz  		.gc_clean
        jmp     	.gc_finish
    .gc_clean:
        mov		    ecx, eax            ; stack alignment start
        mov		    eax, ebp
        sub		    eax, esp
        xor		    edx, edx
        mov		    ebx, 16
        div		    ebx
        mov		    eax, 16
        sub		    eax, edx
        add		    eax, 12
        sub		    esp, eax
        push		eax                 ; stack alignment finish
        push		ecx
        call		_free
        add		    esp, 4
        pop		    ebx                 ; restore stack alignment start
        add		    esp, ebx            ; restore stack alignment finish
    .gc_finish:
        ret
    .gc_increment:
        cmp		    ebx, 5              ; compare type to boxed array (id = 5)
        jz  		.gc_finish
        sub		    eax, 2              ; store pointers counter in first two bytes of heap object
        mov		    bx, word [eax]
        add		    bx, 1               ; pointers counter increment
        mov		    word [eax], bx
        jmp         .gc_finish
