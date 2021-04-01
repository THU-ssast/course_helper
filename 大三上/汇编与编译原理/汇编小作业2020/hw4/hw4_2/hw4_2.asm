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
targetStr BYTE "ABCDE", 10 DUP(0)
sourceStr BYTE "FGH", 0

.code
;----------------
;ShowParams
;----------------
Str_concat PROC,
	target: DWORD, source: DWORD

	mov eax, target
	.REPEAT 
	inc eax
	mov ebx, [eax]
	.UNTIL ebx==0

	mov edx, source
	.REPEAT 
	mov esi, [edx]
	mov [eax], esi
	inc eax
	inc edx
	.UNTIL esi==0

    ret
Str_concat ENDP


main PROC
	INVOKE Str_concat, ADDR targetStr, ADDR sourceStr
	INVOKE printf, offset targetStr
    INVOKE ExitProcess, 0
main ENDP

END main