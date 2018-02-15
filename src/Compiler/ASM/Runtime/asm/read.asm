SECTION .bss
    read_buffer		    resb 255
    read_buffer_done	resb 4
    read_buffer_all		resb 4

SECTION .text
    global read
    read:
        mov     eax, 3
        push    255             ; read buffer size
        push    read_buffer     ; read buffer pointer
        push    0
        push    eax
        int     0x80
        add     esp, 16
        mov     [read_buffer_all], eax
        ret