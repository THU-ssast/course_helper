.386
.model flat, stdcall
option casemap:none
include windows.inc
include kernel32.inc
include user32.inc
includelib kernel32.lib
includelib user32.lib
includelib      msvcrt.lib
printf          PROTO C :ptr sbyte, :VARARG
scanf           PROTO C :ptr sbyte, :VARARG

.data
ansMsg  byte "%d", 0ah, 0dh, 0
myArray WORD 3, 1, 7, 5, 2, 9, 4, 3


.code
;----------------
;BubbleSort
;----------------
BubbleSort PROC,
	Array: DWORD,
	array_length: DWORD

	mov ecx, array_length
	sub ecx, 1
	;---------------outer loop--------------------
	L1:                    
	push ecx	
	mov eax, Array
	mov edi, 0             ;edi is used to identify whether swap
	;---------------inner loop--------------------
	L2:                    
	mov edx, eax
	add edx, 2
	mov si, [eax]
	mov bx, [edx]

	.IF si>bx              ;swap 
	mov edi, 1
	mov [edx], si
	mov [eax], bx
	.ENDIF

	add eax, 2
	loop L2
	;---------------inner loop--------------------
	.IF edi==0             ;judge whether to quit sorting
	jmp FI                 
	.ENDIF

	pop ecx
	loop L1
	;---------------outer loop--------------------
	FI:
    ret
BubbleSort ENDP


main PROC
	INVOKE BubbleSort, ADDR myArray, 8
	mov eax, offset myArray
	mov ecx, 8

	L3:
	pushad
	mov bx, [eax]
	INVOKE printf, offset ansMsg, bx
	popad
	add eax, 2
	loop L3

    INVOKE ExitProcess, 0
main ENDP

END main