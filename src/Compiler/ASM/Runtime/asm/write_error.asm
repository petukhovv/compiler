%define STDERR              2
%define WRITE_SYS_CALL      4

global write_error
write_error:
    push    ebx                 ; value size
    push    eax                 ; pointer to the value
    push    STDERR              ; file descriptor 2 = STDERR
    mov     eax, WRITE_SYS_CALL ; 'write' system call = 4
    sub     esp, 4              ; align the stack by moving the stack pointer 4 more bytes (16 - 4 * 3)
    int     0x80                ; interrupt of the syscall type
    add     esp, 20             ; restore stack state
    ret