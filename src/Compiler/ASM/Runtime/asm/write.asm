%define STDOUT              1
%define WRITE_SYS_CALL      4

global write
write:
    push    eax
    mov     eax, esp            ; store value (from eax) address (= current stack position)
    push    1                   ; value size = 1 byte (byte-by-byte write, see itoa_and_write.asm)
    push    eax                 ; pointer to the value
    push    STDOUT              ; file descriptor 1 = STDOUT
    mov     eax, WRITE_SYS_CALL ; 'write' system call = 4
    sub     esp, 4              ; align the stack by moving the stack pointer 4 more bytes (16 - 4 * 3)
    int     0x80                ; interrupt of the syscall type
    add     esp, 20             ; restore stack state
    ret