.386
.model flat, stdcall
option casemap:none
include windows.inc
include kernel32.inc
include user32.inc
includelib kernel32.lib
includelib user32.lib
includelib msvcrt.lib

printf          PROTO C :ptr sbyte, :VARARG
scanf           PROTO C :ptr sbyte, :VARARG
WriteInt        PROTO

mWriteInt MACRO number
	mov ebx, TYPE number
	.if ebx == 1 
	mov eax, 0
	mov al, byte ptr number
	.elseif ebx == 2
	mov eax, 0
	mov ax, word ptr number
	.elseif ebx == 4
	mov eax, dword ptr number
	.endif
	call WriteInt
ENDM

.data
test_byte BYTE 9
test_word WORD 19
test_dword DWORD 29

.code
main PROC
	mWriteInt test_byte
	mWriteInt test_word
	mWriteInt test_dword

    INVOKE ExitProcess, 0
main ENDP

END main