class Registers:
    # 8-bit registers
    AH = 'ah'
    AL = 'al'
    CH = 'ch'
    CL = 'cl'
    DH = 'dh'
    DL = 'dl'
    BH = 'bh'
    BL = 'bl'

    # 16-bit registers
    AX = 'ax'
    CX = 'cx'
    DX = 'dx'
    BX = 'bx'
    SP = 'sp'
    BP = 'bp'
    SI = 'si'
    DI = 'di'

    # 32-bit registers
    EAX = 'eax'
    ECX = 'ecx'
    EDX = 'edx'
    EBX = 'ebx'
    ESP = 'esp'
    EBP = 'ebp'
    ESI = 'esi'
    EDI = 'edi'

    # Used 32-bit ASM, but you can extend the list of registers and start using 64-bit registers
