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
vala dword 0h
valb sword 0h
valc byte 0h
ansMsg byte "½á¹ûÊÇ%d", 0ah, 0dh, 0

.code
main PROC
	mov eax, TYPE vala
	INVOKE printf, offset ansMsg, eax
	mov eax, TYPE valb
	INVOKE printf, offset ansMsg, eax	
	mov eax, TYPE valc
	INVOKE printf, offset ansMsg, eax

    INVOKE ExitProcess, 0
main ENDP

END main