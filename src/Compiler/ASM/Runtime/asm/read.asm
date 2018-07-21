%define STDIN               0
%define READ_SYS_CALL       3
%define MAX_BUFFER_SIZE     65536

SECTION .bss
    read_buffer		    resb    MAX_BUFFER_SIZE     ; max read buffer size = 64KB
    read_buffer_offset	resw    1                   ; read buffer offset size = 2B (max offset = 65535 = max buffer size)
    read_buffer_size	resw    1                   ; read buffer size = 2B (65535 = max buffer size)

SECTION .text
    global read
    read:
        push    MAX_BUFFER_SIZE         ; read buffer size
        push    read_buffer             ; read buffer pointer
        push    STDIN                   ; file descriptor 0 = STDIN
        mov     eax, READ_SYS_CALL      ; 'read' system call = 4
        sub     esp, 4                  ; align the stack by moving the stack pointer 4 more bytes (16 - 4 * 3)
        int     0x80                    ; interrupt of the syscall type
        add     esp, 16                 ; restore stack state
        mov     [read_buffer_size], ax  ; write the number of bytes read in the ax register
        ret