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
queryMsg          byte    "%d和%d", 0
ansMsg          byte    "结果是%d", 0ah, 0dh, 0

.code
main PROC
	mov eax, 40
	mov ebx, 16
	pushad
	invoke  printf, offset queryMsg, eax, ebx
	popad
	call gcd
	invoke  printf, offset ansMsg, eax

	mov eax, -100
	mov ebx, 16
	pushad
	invoke  printf, offset queryMsg, eax, ebx
	popad
	call gcd
	invoke  printf, offset ansMsg, eax

	mov eax, -140
	mov ebx, -42
	pushad
	invoke  printf, offset queryMsg, eax, ebx
	popad
	call gcd
	invoke  printf, offset ansMsg, eax

    INVOKE ExitProcess, 0
main ENDP

gcd PROC
	;get absolute number
	test eax, 80000000h
	jz notneg1
	neg eax
	notneg1:
	test ebx, 80000000h
	jz notneg2
	neg ebx
	notneg2:

	;do while
	.REPEAT
	mov edx, 0
	div ebx
	mov eax, ebx
	mov ebx, edx
	.UNTIL ebx <= 0

	ret

gcd ENDP


END main