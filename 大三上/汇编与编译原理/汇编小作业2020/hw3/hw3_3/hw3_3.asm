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
ansMsg          byte    "Fib(%d)=%d", 0ah, 0dh, 0

.code
main PROC
	invoke  printf, offset ansMsg, 1, 1
	invoke  printf, offset ansMsg, 2, 1

	mov eax, 1
	mov ebx, 1
	mov ecx, 8

	L1:
	add eax, ebx
	mov esi, eax
	mov eax, ebx
	mov ebx, esi

	;print result
	pushad
	mov edx, 11
	sub edx, ecx
	invoke  printf, offset ansMsg, edx, ebx
	popad

	loop L1

    INVOKE ExitProcess, 0
main ENDP


END main