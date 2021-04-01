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
varA dword 5
varB dword 6
sum DWORD 0
product DWORD 0
ansMsg byte "½á¹ûÊÇ%d", 0ah, 0dh, 0

.code
main PROC
	mov eax, varA
	add eax, varB
	mov sum, eax
	mov eax, varA
	mul varB
	mov product, eax
	INVOKE printf, offset ansMsg, sum
	INVOKE printf, offset ansMsg, product
    INVOKE ExitProcess, 0
main ENDP

END main