_atoi:
	xor	edx, edx
	mov	dl, byte [esi]
	test	dl, dl
	jz	._atoi_exit
	cmp dl, 10          ; 10 - ASCII code of EOL
	je ._atoi_exit
	imul	eax, 10
	sub	dl, 48          ; 48 - ASCII code of 0
	add	eax, edx
	inc	esi
	jmp	_atoi
._atoi_exit:
	ret