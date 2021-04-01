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
ansMsg byte "%s", 0ah, 0dh, 0
source BYTE 'This is the source string', 0
target BYTE SIZEOF source DUP('#')



.code
main PROC
	;×Ö·û´®Ñ¹Õ»
	mov ecx, lengthof source -1
	mov esi, 0
	L1:
	movzx eax, source[esi]
	push eax
	inc esi
	loop L1

	;×Ö·û´®³öÕ»
	mov ecx, lengthof source -1
	mov esi, 0
	L2:
	pop eax
	mov target[esi], al
	inc esi
	loop L2

	;ÊÖ¶¯ÔÚÄ©Î²Ìí¼Ó0
	mov target[esi], 0

	invoke  printf, offset ansMsg, offset target
    INVOKE ExitProcess, 0
main ENDP


END main